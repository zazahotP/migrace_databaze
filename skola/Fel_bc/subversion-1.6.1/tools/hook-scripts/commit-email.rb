#!/usr/bin/env ruby

require 'English'

original_argv = ARGV.dup
argv = []

found_include_option = false
while (arg = original_argv.shift)
  if found_include_option
    $LOAD_PATH.unshift(arg)
    found_include_option = false
  else
    case arg
    when "-I", "--include"
      found_include_option = true
    when /\A-I/, /\A--include=?/
      path = $POSTMATCH
      $LOAD_PATH.unshift(path) unless path.empty?
    else
      argv << arg
    end
  end
end

def extract_email_address(address)
  if /<(.+?)>/ =~ address
    $1
  else
    address
  end
end

def sendmail(to, from, mail, server=nil, port=nil)
  server ||= "localhost"
  from = extract_email_address(from)
  to = to.collect {|address| extract_email_address(address)}
  Net::SMTP.start(server, port) do |smtp|
    smtp.open_message_stream(from, to) do |f|
      f.print(mail)
    end
  end
end

begin
  require 'svn/commit-mailer'
  Svn::Locale.set
  Svn::CommitMailer.run(argv)
rescue Exception => error
  require 'net/smtp'
  require 'socket'

  to = []
  subject = "Error"
  from = "#{ENV['USER']}@#{Socket.gethostname}"
  server = nil
  port = nil
  begin
    begin
      Svn::CommitMailer
    rescue NameError
      raise OptionParser::ParseError
    end
    _, _, _to, options = Svn::CommitMailer.parse(argv)
    to = [_to]
    to = options.error_to unless options.error_to.empty?
    from = options.from || from
    subject = "#{options.name}: #{subject}" if options.name
    server = options.server
    port = options.port
  rescue OptionParser::MissingArgument
    argv.delete_if {|arg| $!.args.include?(arg)}
    retry
  rescue OptionParser::ParseError
    if to.empty?
      _, _, _to, *_ = ARGV.reject {|arg| /^-/.match(arg)}
      to = [_to]
    end
  end

  detail = <<-EOM
#{error.class}: #{error.message}
#{error.backtrace.join("\n")}
EOM
  to = to.compact
  if to.empty?
    STDERR.puts detail
  else
    sendmail(to, from, <<-MAIL, server, port)
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
From: #{from}
To: #{to.join(', ')}
Subject: #{subject}
Date: #{Time.now.rfc2822}

#{detail}
MAIL
  end
end
