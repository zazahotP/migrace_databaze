﻿#pragma warning disable 1591
//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//     Runtime Version:2.0.50727.4927
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace BLL
{
	using System.Data.Linq;
	using System.Data.Linq.Mapping;
	using System.Data;
	using System.Collections.Generic;
	using System.Reflection;
	using System.Linq;
	using System.Linq.Expressions;
	using System.ComponentModel;
	using System;
	
	
	public partial class MFlowDB : System.Data.Linq.DataContext
	{
		
		private static System.Data.Linq.Mapping.MappingSource mappingSource = new AttributeMappingSource();
		
    #region Extensibility Method Definitions
    partial void OnCreated();
    partial void InsertAccount(Account instance);
    partial void UpdateAccount(Account instance);
    partial void DeleteAccount(Account instance);
    partial void InsertCashed(Cashed instance);
    partial void UpdateCashed(Cashed instance);
    partial void DeleteCashed(Cashed instance);
    partial void InsertCategory(Category instance);
    partial void UpdateCategory(Category instance);
    partial void DeleteCategory(Category instance);
    partial void InsertItem(Item instance);
    partial void UpdateItem(Item instance);
    partial void DeleteItem(Item instance);
    partial void InsertMonitoring(Monitoring instance);
    partial void UpdateMonitoring(Monitoring instance);
    partial void DeleteMonitoring(Monitoring instance);
    partial void InsertProfile(Profile instance);
    partial void UpdateProfile(Profile instance);
    partial void DeleteProfile(Profile instance);
    partial void InsertStopper(Stopper instance);
    partial void UpdateStopper(Stopper instance);
    partial void DeleteStopper(Stopper instance);
    #endregion
		
		public MFlowDB(string connection) : 
				base(connection, mappingSource)
		{
			OnCreated();
		}
		
		public MFlowDB(System.Data.IDbConnection connection) : 
				base(connection, mappingSource)
		{
			OnCreated();
		}
		
		public MFlowDB(string connection, System.Data.Linq.Mapping.MappingSource mappingSource) : 
				base(connection, mappingSource)
		{
			OnCreated();
		}
		
		public MFlowDB(System.Data.IDbConnection connection, System.Data.Linq.Mapping.MappingSource mappingSource) : 
				base(connection, mappingSource)
		{
			OnCreated();
		}
		
		public System.Data.Linq.Table<Account> Account
		{
			get
			{
				return this.GetTable<Account>();
			}
		}
		
		public System.Data.Linq.Table<Cashed> Cashed
		{
			get
			{
				return this.GetTable<Cashed>();
			}
		}
		
		public System.Data.Linq.Table<Category> Category
		{
			get
			{
				return this.GetTable<Category>();
			}
		}
		
		public System.Data.Linq.Table<Item> Item
		{
			get
			{
				return this.GetTable<Item>();
			}
		}
		
		public System.Data.Linq.Table<Monitoring> Monitoring
		{
			get
			{
				return this.GetTable<Monitoring>();
			}
		}
		
		public System.Data.Linq.Table<Profile> Profile
		{
			get
			{
				return this.GetTable<Profile>();
			}
		}
		
		public System.Data.Linq.Table<Stopper> Stopper
		{
			get
			{
				return this.GetTable<Stopper>();
			}
		}
	}
	
	[Table()]
	public partial class Account : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private int _Account_id;
		
		private string _Pass;
		
		private string _Nick;
		
		private string _Name;
		
		private EntitySet<Profile> _Profile;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnAccount_idChanging(int value);
    partial void OnAccount_idChanged();
    partial void OnPassChanging(string value);
    partial void OnPassChanged();
    partial void OnNickChanging(string value);
    partial void OnNickChanged();
    partial void OnNameChanging(string value);
    partial void OnNameChanged();
    #endregion
		
		public Account()
		{
			this._Profile = new EntitySet<Profile>(new Action<Profile>(this.attach_Profile), new Action<Profile>(this.detach_Profile));
			OnCreated();
		}
		
		[Column(Name="account_id", Storage="_Account_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Account_id
		{
			get
			{
				return this._Account_id;
			}
			set
			{
				if ((this._Account_id != value))
				{
					this.OnAccount_idChanging(value);
					this.SendPropertyChanging();
					this._Account_id = value;
					this.SendPropertyChanged("Account_id");
					this.OnAccount_idChanged();
				}
			}
		}
		
		[Column(Name="pass", Storage="_Pass", DbType="NVarChar(20) NOT NULL", CanBeNull=false)]
		public string Pass
		{
			get
			{
				return this._Pass;
			}
			set
			{
				if ((this._Pass != value))
				{
					this.OnPassChanging(value);
					this.SendPropertyChanging();
					this._Pass = value;
					this.SendPropertyChanged("Pass");
					this.OnPassChanged();
				}
			}
		}
		
		[Column(Name="nick", Storage="_Nick", DbType="NVarChar(20) NOT NULL", CanBeNull=false)]
		public string Nick
		{
			get
			{
				return this._Nick;
			}
			set
			{
				if ((this._Nick != value))
				{
					this.OnNickChanging(value);
					this.SendPropertyChanging();
					this._Nick = value;
					this.SendPropertyChanged("Nick");
					this.OnNickChanged();
				}
			}
		}
		
		[Column(Name="name", Storage="_Name", DbType="NVarChar(50)")]
		public string Name
		{
			get
			{
				return this._Name;
			}
			set
			{
				if ((this._Name != value))
				{
					this.OnNameChanging(value);
					this.SendPropertyChanging();
					this._Name = value;
					this.SendPropertyChanged("Name");
					this.OnNameChanged();
				}
			}
		}
		
		[Association(Name="Account_Profile", Storage="_Profile", ThisKey="Account_id", OtherKey="Account_id")]
		public EntitySet<Profile> Profile
		{
			get
			{
				return this._Profile;
			}
			set
			{
				this._Profile.Assign(value);
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
		
		private void attach_Profile(Profile entity)
		{
			this.SendPropertyChanging();
			entity.Account = this;
		}
		
		private void detach_Profile(Profile entity)
		{
			this.SendPropertyChanging();
			entity.Account = null;
		}
	}
	
	[Table()]
	public partial class Cashed : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private System.DateTime _Paid;
		
		private string _Cashtype;
		
		private int _Category_id;
		
		private int _Item_id;
		
		private EntityRef<Category> _Category;
		
		private EntityRef<Item> _Item;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnPaidChanging(System.DateTime value);
    partial void OnPaidChanged();
    partial void OnCashtypeChanging(string value);
    partial void OnCashtypeChanged();
    partial void OnCategory_idChanging(int value);
    partial void OnCategory_idChanged();
    partial void OnItem_idChanging(int value);
    partial void OnItem_idChanged();
    #endregion
		
		public Cashed()
		{
			this._Category = default(EntityRef<Category>);
			this._Item = default(EntityRef<Item>);
			OnCreated();
		}
		
		[Column(Name="paid", Storage="_Paid", DbType="DateTime NOT NULL", IsPrimaryKey=true)]
		public System.DateTime Paid
		{
			get
			{
				return this._Paid;
			}
			set
			{
				if ((this._Paid != value))
				{
					this.OnPaidChanging(value);
					this.SendPropertyChanging();
					this._Paid = value;
					this.SendPropertyChanged("Paid");
					this.OnPaidChanged();
				}
			}
		}
		
		[Column(Name="cashtype", Storage="_Cashtype", DbType="NVarChar(10) NOT NULL", CanBeNull=false, IsPrimaryKey=true)]
		public string Cashtype
		{
			get
			{
				return this._Cashtype;
			}
			set
			{
				if ((this._Cashtype != value))
				{
					this.OnCashtypeChanging(value);
					this.SendPropertyChanging();
					this._Cashtype = value;
					this.SendPropertyChanged("Cashtype");
					this.OnCashtypeChanged();
				}
			}
		}
		
		[Column(Name="category_id", Storage="_Category_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Category_id
		{
			get
			{
				return this._Category_id;
			}
			set
			{
				if ((this._Category_id != value))
				{
					this.OnCategory_idChanging(value);
					this.SendPropertyChanging();
					this._Category_id = value;
					this.SendPropertyChanged("Category_id");
					this.OnCategory_idChanged();
				}
			}
		}
		
		[Column(Name="item_id", Storage="_Item_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Item_id
		{
			get
			{
				return this._Item_id;
			}
			set
			{
				if ((this._Item_id != value))
				{
					this.OnItem_idChanging(value);
					this.SendPropertyChanging();
					this._Item_id = value;
					this.SendPropertyChanged("Item_id");
					this.OnItem_idChanged();
				}
			}
		}
		
		[Association(Name="Category_Cashed", Storage="_Category", ThisKey="Category_id", OtherKey="Category_id", IsForeignKey=true)]
		public Category Category
		{
			get
			{
				return this._Category.Entity;
			}
			set
			{
				Category previousValue = this._Category.Entity;
				if (((previousValue != value) 
							|| (this._Category.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Category.Entity = null;
						previousValue.Cashed.Remove(this);
					}
					this._Category.Entity = value;
					if ((value != null))
					{
						value.Cashed.Add(this);
						this._Category_id = value.Category_id;
					}
					else
					{
						this._Category_id = default(int);
					}
					this.SendPropertyChanged("Category");
				}
			}
		}
		
		[Association(Name="Item_Cashed", Storage="_Item", ThisKey="Item_id", OtherKey="Item_id", IsForeignKey=true)]
		public Item Item
		{
			get
			{
				return this._Item.Entity;
			}
			set
			{
				Item previousValue = this._Item.Entity;
				if (((previousValue != value) 
							|| (this._Item.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Item.Entity = null;
						previousValue.Cashed.Remove(this);
					}
					this._Item.Entity = value;
					if ((value != null))
					{
						value.Cashed.Add(this);
						this._Item_id = value.Item_id;
					}
					else
					{
						this._Item_id = default(int);
					}
					this.SendPropertyChanged("Item");
				}
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
	}
	
	[Table()]
	public partial class Category : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private System.Nullable<int> _Sup_category_id;
		
		private int _Profile_id;
		
		private int _Category_id;
		
		private string _Name;
		
		private string _Description;
		
		private EntitySet<Cashed> _Cashed;
		
		private EntitySet<Category> _Category_;
		
		private EntitySet<Monitoring> _Monitoring;
		
		private EntityRef<Category> _Sup_category_;
		
		private EntityRef<Profile> _Profile;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnSup_category_idChanging(System.Nullable<int> value);
    partial void OnSup_category_idChanged();
    partial void OnProfile_idChanging(int value);
    partial void OnProfile_idChanged();
    partial void OnCategory_idChanging(int value);
    partial void OnCategory_idChanged();
    partial void OnNameChanging(string value);
    partial void OnNameChanged();
    partial void OnDescriptionChanging(string value);
    partial void OnDescriptionChanged();
    #endregion
		
		public Category()
		{
			this._Cashed = new EntitySet<Cashed>(new Action<Cashed>(this.attach_Cashed), new Action<Cashed>(this.detach_Cashed));
			this._Category_ = new EntitySet<Category>(new Action<Category>(this.attach_Category_), new Action<Category>(this.detach_Category_));
			this._Monitoring = new EntitySet<Monitoring>(new Action<Monitoring>(this.attach_Monitoring), new Action<Monitoring>(this.detach_Monitoring));
			this._Sup_category_ = default(EntityRef<Category>);
			this._Profile = default(EntityRef<Profile>);
			OnCreated();
		}
		
		[Column(Name="sup_category_id", Storage="_Sup_category_id", DbType="Int")]
		public System.Nullable<int> Sup_category_id
		{
			get
			{
				return this._Sup_category_id;
			}
			set
			{
				if ((this._Sup_category_id != value))
				{
					this.OnSup_category_idChanging(value);
					this.SendPropertyChanging();
					this._Sup_category_id = value;
					this.SendPropertyChanged("Sup_category_id");
					this.OnSup_category_idChanged();
				}
			}
		}
		
		[Column(Name="profile_id", Storage="_Profile_id", DbType="Int NOT NULL")]
		public int Profile_id
		{
			get
			{
				return this._Profile_id;
			}
			set
			{
				if ((this._Profile_id != value))
				{
					this.OnProfile_idChanging(value);
					this.SendPropertyChanging();
					this._Profile_id = value;
					this.SendPropertyChanged("Profile_id");
					this.OnProfile_idChanged();
				}
			}
		}
		
		[Column(Name="category_id", Storage="_Category_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Category_id
		{
			get
			{
				return this._Category_id;
			}
			set
			{
				if ((this._Category_id != value))
				{
					this.OnCategory_idChanging(value);
					this.SendPropertyChanging();
					this._Category_id = value;
					this.SendPropertyChanged("Category_id");
					this.OnCategory_idChanged();
				}
			}
		}
		
		[Column(Name="name", Storage="_Name", DbType="NVarChar(20) NOT NULL", CanBeNull=false)]
		public string Name
		{
			get
			{
				return this._Name;
			}
			set
			{
				if ((this._Name != value))
				{
					this.OnNameChanging(value);
					this.SendPropertyChanging();
					this._Name = value;
					this.SendPropertyChanged("Name");
					this.OnNameChanged();
				}
			}
		}
		
		[Column(Name="description", Storage="_Description", DbType="NVarChar(500)")]
		public string Description
		{
			get
			{
				return this._Description;
			}
			set
			{
				if ((this._Description != value))
				{
					this.OnDescriptionChanging(value);
					this.SendPropertyChanging();
					this._Description = value;
					this.SendPropertyChanged("Description");
					this.OnDescriptionChanged();
				}
			}
		}
		
		[Association(Name="Category_Cashed", Storage="_Cashed", ThisKey="Category_id", OtherKey="Category_id")]
		public EntitySet<Cashed> Cashed
		{
			get
			{
				return this._Cashed;
			}
			set
			{
				this._Cashed.Assign(value);
			}
		}
		
		[Association(Name="Category_Category", Storage="_Category_", ThisKey="Category_id", OtherKey="Sup_category_id")]
		public EntitySet<Category> Category_
		{
			get
			{
				return this._Category_;
			}
			set
			{
				this._Category_.Assign(value);
			}
		}
		
		[Association(Name="Category_Monitoring", Storage="_Monitoring", ThisKey="Category_id", OtherKey="Category_id")]
		public EntitySet<Monitoring> Monitoring
		{
			get
			{
				return this._Monitoring;
			}
			set
			{
				this._Monitoring.Assign(value);
			}
		}
		
		[Association(Name="Category_Category", Storage="_Sup_category_", ThisKey="Sup_category_id", OtherKey="Category_id", IsForeignKey=true)]
		public Category Sup_category_
		{
			get
			{
				return this._Sup_category_.Entity;
			}
			set
			{
				Category previousValue = this._Sup_category_.Entity;
				if (((previousValue != value) 
							|| (this._Sup_category_.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Sup_category_.Entity = null;
						previousValue.Category_.Remove(this);
					}
					this._Sup_category_.Entity = value;
					if ((value != null))
					{
						value.Category_.Add(this);
						this._Sup_category_id = value.Category_id;
					}
					else
					{
						this._Sup_category_id = default(Nullable<int>);
					}
					this.SendPropertyChanged("Sup_category_");
				}
			}
		}
		
		[Association(Name="Profile_Category", Storage="_Profile", ThisKey="Profile_id", OtherKey="Profile_id", IsForeignKey=true)]
		public Profile Profile
		{
			get
			{
				return this._Profile.Entity;
			}
			set
			{
				Profile previousValue = this._Profile.Entity;
				if (((previousValue != value) 
							|| (this._Profile.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Profile.Entity = null;
						previousValue.Category.Remove(this);
					}
					this._Profile.Entity = value;
					if ((value != null))
					{
						value.Category.Add(this);
						this._Profile_id = value.Profile_id;
					}
					else
					{
						this._Profile_id = default(int);
					}
					this.SendPropertyChanged("Profile");
				}
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
		
		private void attach_Cashed(Cashed entity)
		{
			this.SendPropertyChanging();
			entity.Category = this;
		}
		
		private void detach_Cashed(Cashed entity)
		{
			this.SendPropertyChanging();
			entity.Category = null;
		}
		
		private void attach_Category_(Category entity)
		{
			this.SendPropertyChanging();
			entity.Sup_category_ = this;
		}
		
		private void detach_Category_(Category entity)
		{
			this.SendPropertyChanging();
			entity.Sup_category_ = null;
		}
		
		private void attach_Monitoring(Monitoring entity)
		{
			this.SendPropertyChanging();
			entity.Category = this;
		}
		
		private void detach_Monitoring(Monitoring entity)
		{
			this.SendPropertyChanging();
			entity.Category = null;
		}
	}
	
	[Table()]
	public partial class Item : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private int _Item_id;
		
		private int _Item_value;
		
		private string _Description;
		
		private EntitySet<Cashed> _Cashed;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnItem_idChanging(int value);
    partial void OnItem_idChanged();
    partial void OnItem_valueChanging(int value);
    partial void OnItem_valueChanged();
    partial void OnDescriptionChanging(string value);
    partial void OnDescriptionChanged();
    #endregion
		
		public Item()
		{
			this._Cashed = new EntitySet<Cashed>(new Action<Cashed>(this.attach_Cashed), new Action<Cashed>(this.detach_Cashed));
			OnCreated();
		}
		
		[Column(Name="item_id", Storage="_Item_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Item_id
		{
			get
			{
				return this._Item_id;
			}
			set
			{
				if ((this._Item_id != value))
				{
					this.OnItem_idChanging(value);
					this.SendPropertyChanging();
					this._Item_id = value;
					this.SendPropertyChanged("Item_id");
					this.OnItem_idChanged();
				}
			}
		}
		
		[Column(Name="item_value", Storage="_Item_value", DbType="Int NOT NULL")]
		public int Item_value
		{
			get
			{
				return this._Item_value;
			}
			set
			{
				if ((this._Item_value != value))
				{
					this.OnItem_valueChanging(value);
					this.SendPropertyChanging();
					this._Item_value = value;
					this.SendPropertyChanged("Item_value");
					this.OnItem_valueChanged();
				}
			}
		}
		
		[Column(Name="description", Storage="_Description", DbType="NVarChar(100)")]
		public string Description
		{
			get
			{
				return this._Description;
			}
			set
			{
				if ((this._Description != value))
				{
					this.OnDescriptionChanging(value);
					this.SendPropertyChanging();
					this._Description = value;
					this.SendPropertyChanged("Description");
					this.OnDescriptionChanged();
				}
			}
		}
		
		[Association(Name="Item_Cashed", Storage="_Cashed", ThisKey="Item_id", OtherKey="Item_id")]
		public EntitySet<Cashed> Cashed
		{
			get
			{
				return this._Cashed;
			}
			set
			{
				this._Cashed.Assign(value);
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
		
		private void attach_Cashed(Cashed entity)
		{
			this.SendPropertyChanging();
			entity.Item = this;
		}
		
		private void detach_Cashed(Cashed entity)
		{
			this.SendPropertyChanging();
			entity.Item = null;
		}
	}
	
	[Table()]
	public partial class Monitoring : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private System.DateTime _From_date;
		
		private System.DateTime _To_date;
		
		private string _Treshold_type;
		
		private int _Category_id;
		
		private int _Stopper_id;
		
		private EntityRef<Category> _Category;
		
		private EntityRef<Stopper> _Stopper;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnFrom_dateChanging(System.DateTime value);
    partial void OnFrom_dateChanged();
    partial void OnTo_dateChanging(System.DateTime value);
    partial void OnTo_dateChanged();
    partial void OnTreshold_typeChanging(string value);
    partial void OnTreshold_typeChanged();
    partial void OnCategory_idChanging(int value);
    partial void OnCategory_idChanged();
    partial void OnStopper_idChanging(int value);
    partial void OnStopper_idChanged();
    #endregion
		
		public Monitoring()
		{
			this._Category = default(EntityRef<Category>);
			this._Stopper = default(EntityRef<Stopper>);
			OnCreated();
		}
		
		[Column(Name="from_date", Storage="_From_date", DbType="DateTime NOT NULL", IsPrimaryKey=true)]
		public System.DateTime From_date
		{
			get
			{
				return this._From_date;
			}
			set
			{
				if ((this._From_date != value))
				{
					this.OnFrom_dateChanging(value);
					this.SendPropertyChanging();
					this._From_date = value;
					this.SendPropertyChanged("From_date");
					this.OnFrom_dateChanged();
				}
			}
		}
		
		[Column(Name="to_date", Storage="_To_date", DbType="DateTime NOT NULL", IsPrimaryKey=true)]
		public System.DateTime To_date
		{
			get
			{
				return this._To_date;
			}
			set
			{
				if ((this._To_date != value))
				{
					this.OnTo_dateChanging(value);
					this.SendPropertyChanging();
					this._To_date = value;
					this.SendPropertyChanged("To_date");
					this.OnTo_dateChanged();
				}
			}
		}
		
		[Column(Name="treshold_type", Storage="_Treshold_type", DbType="NVarChar(10) NOT NULL", CanBeNull=false, IsPrimaryKey=true)]
		public string Treshold_type
		{
			get
			{
				return this._Treshold_type;
			}
			set
			{
				if ((this._Treshold_type != value))
				{
					this.OnTreshold_typeChanging(value);
					this.SendPropertyChanging();
					this._Treshold_type = value;
					this.SendPropertyChanged("Treshold_type");
					this.OnTreshold_typeChanged();
				}
			}
		}
		
		[Column(Name="category_id", Storage="_Category_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Category_id
		{
			get
			{
				return this._Category_id;
			}
			set
			{
				if ((this._Category_id != value))
				{
					this.OnCategory_idChanging(value);
					this.SendPropertyChanging();
					this._Category_id = value;
					this.SendPropertyChanged("Category_id");
					this.OnCategory_idChanged();
				}
			}
		}
		
		[Column(Name="stopper_id", Storage="_Stopper_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Stopper_id
		{
			get
			{
				return this._Stopper_id;
			}
			set
			{
				if ((this._Stopper_id != value))
				{
					this.OnStopper_idChanging(value);
					this.SendPropertyChanging();
					this._Stopper_id = value;
					this.SendPropertyChanged("Stopper_id");
					this.OnStopper_idChanged();
				}
			}
		}
		
		[Association(Name="Category_Monitoring", Storage="_Category", ThisKey="Category_id", OtherKey="Category_id", IsForeignKey=true)]
		public Category Category
		{
			get
			{
				return this._Category.Entity;
			}
			set
			{
				Category previousValue = this._Category.Entity;
				if (((previousValue != value) 
							|| (this._Category.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Category.Entity = null;
						previousValue.Monitoring.Remove(this);
					}
					this._Category.Entity = value;
					if ((value != null))
					{
						value.Monitoring.Add(this);
						this._Category_id = value.Category_id;
					}
					else
					{
						this._Category_id = default(int);
					}
					this.SendPropertyChanged("Category");
				}
			}
		}
		
		[Association(Name="Stopper_Monitoring", Storage="_Stopper", ThisKey="Stopper_id", OtherKey="Stopper_id", IsForeignKey=true)]
		public Stopper Stopper
		{
			get
			{
				return this._Stopper.Entity;
			}
			set
			{
				Stopper previousValue = this._Stopper.Entity;
				if (((previousValue != value) 
							|| (this._Stopper.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Stopper.Entity = null;
						previousValue.Monitoring.Remove(this);
					}
					this._Stopper.Entity = value;
					if ((value != null))
					{
						value.Monitoring.Add(this);
						this._Stopper_id = value.Stopper_id;
					}
					else
					{
						this._Stopper_id = default(int);
					}
					this.SendPropertyChanged("Stopper");
				}
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
	}
	
	[Table()]
	public partial class Profile : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private int _Account_id;
		
		private int _Profile_id;
		
		private string _Type;
		
		private string _Description;
		
		private string _Name;
		
		private EntitySet<Category> _Category;
		
		private EntityRef<Account> _Account;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnAccount_idChanging(int value);
    partial void OnAccount_idChanged();
    partial void OnProfile_idChanging(int value);
    partial void OnProfile_idChanged();
    partial void OnTypeChanging(string value);
    partial void OnTypeChanged();
    partial void OnDescriptionChanging(string value);
    partial void OnDescriptionChanged();
    partial void OnNameChanging(string value);
    partial void OnNameChanged();
    #endregion
		
		public Profile()
		{
			this._Category = new EntitySet<Category>(new Action<Category>(this.attach_Category), new Action<Category>(this.detach_Category));
			this._Account = default(EntityRef<Account>);
			OnCreated();
		}
		
		[Column(Name="account_id", Storage="_Account_id", DbType="Int NOT NULL")]
		public int Account_id
		{
			get
			{
				return this._Account_id;
			}
			set
			{
				if ((this._Account_id != value))
				{
					this.OnAccount_idChanging(value);
					this.SendPropertyChanging();
					this._Account_id = value;
					this.SendPropertyChanged("Account_id");
					this.OnAccount_idChanged();
				}
			}
		}
		
		[Column(Name="profile_id", Storage="_Profile_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Profile_id
		{
			get
			{
				return this._Profile_id;
			}
			set
			{
				if ((this._Profile_id != value))
				{
					this.OnProfile_idChanging(value);
					this.SendPropertyChanging();
					this._Profile_id = value;
					this.SendPropertyChanged("Profile_id");
					this.OnProfile_idChanged();
				}
			}
		}
		
		[Column(Name="type", Storage="_Type", DbType="NVarChar(20)")]
		public string Type
		{
			get
			{
				return this._Type;
			}
			set
			{
				if ((this._Type != value))
				{
					this.OnTypeChanging(value);
					this.SendPropertyChanging();
					this._Type = value;
					this.SendPropertyChanged("Type");
					this.OnTypeChanged();
				}
			}
		}
		
		[Column(Name="description", Storage="_Description", DbType="NVarChar(500)")]
		public string Description
		{
			get
			{
				return this._Description;
			}
			set
			{
				if ((this._Description != value))
				{
					this.OnDescriptionChanging(value);
					this.SendPropertyChanging();
					this._Description = value;
					this.SendPropertyChanged("Description");
					this.OnDescriptionChanged();
				}
			}
		}
		
		[Column(Name="name", Storage="_Name", DbType="NVarChar(20) NOT NULL", CanBeNull=false)]
		public string Name
		{
			get
			{
				return this._Name;
			}
			set
			{
				if ((this._Name != value))
				{
					this.OnNameChanging(value);
					this.SendPropertyChanging();
					this._Name = value;
					this.SendPropertyChanged("Name");
					this.OnNameChanged();
				}
			}
		}
		
		[Association(Name="Profile_Category", Storage="_Category", ThisKey="Profile_id", OtherKey="Profile_id")]
		public EntitySet<Category> Category
		{
			get
			{
				return this._Category;
			}
			set
			{
				this._Category.Assign(value);
			}
		}
		
		[Association(Name="Account_Profile", Storage="_Account", ThisKey="Account_id", OtherKey="Account_id", IsForeignKey=true)]
		public Account Account
		{
			get
			{
				return this._Account.Entity;
			}
			set
			{
				Account previousValue = this._Account.Entity;
				if (((previousValue != value) 
							|| (this._Account.HasLoadedOrAssignedValue == false)))
				{
					this.SendPropertyChanging();
					if ((previousValue != null))
					{
						this._Account.Entity = null;
						previousValue.Profile.Remove(this);
					}
					this._Account.Entity = value;
					if ((value != null))
					{
						value.Profile.Add(this);
						this._Account_id = value.Account_id;
					}
					else
					{
						this._Account_id = default(int);
					}
					this.SendPropertyChanged("Account");
				}
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
		
		private void attach_Category(Category entity)
		{
			this.SendPropertyChanging();
			entity.Profile = this;
		}
		
		private void detach_Category(Category entity)
		{
			this.SendPropertyChanging();
			entity.Profile = null;
		}
	}
	
	[Table()]
	public partial class Stopper : INotifyPropertyChanging, INotifyPropertyChanged
	{
		
		private static PropertyChangingEventArgs emptyChangingEventArgs = new PropertyChangingEventArgs(String.Empty);
		
		private int _Stopper_id;
		
		private string _Reason;
		
		private double _Treshold_value;
		
		private System.Nullable<int> _Warning_value;
		
		private System.Nullable<int> _Caution_value;
		
		private EntitySet<Monitoring> _Monitoring;
		
    #region Extensibility Method Definitions
    partial void OnLoaded();
    partial void OnValidate(System.Data.Linq.ChangeAction action);
    partial void OnCreated();
    partial void OnStopper_idChanging(int value);
    partial void OnStopper_idChanged();
    partial void OnReasonChanging(string value);
    partial void OnReasonChanged();
    partial void OnTreshold_valueChanging(double value);
    partial void OnTreshold_valueChanged();
    partial void OnWarning_valueChanging(System.Nullable<int> value);
    partial void OnWarning_valueChanged();
    partial void OnCaution_valueChanging(System.Nullable<int> value);
    partial void OnCaution_valueChanged();
    #endregion
		
		public Stopper()
		{
			this._Monitoring = new EntitySet<Monitoring>(new Action<Monitoring>(this.attach_Monitoring), new Action<Monitoring>(this.detach_Monitoring));
			OnCreated();
		}
		
		[Column(Name="stopper_id", Storage="_Stopper_id", DbType="Int NOT NULL", IsPrimaryKey=true)]
		public int Stopper_id
		{
			get
			{
				return this._Stopper_id;
			}
			set
			{
				if ((this._Stopper_id != value))
				{
					this.OnStopper_idChanging(value);
					this.SendPropertyChanging();
					this._Stopper_id = value;
					this.SendPropertyChanged("Stopper_id");
					this.OnStopper_idChanged();
				}
			}
		}
		
		[Column(Name="reason", Storage="_Reason", DbType="NVarChar(255)")]
		public string Reason
		{
			get
			{
				return this._Reason;
			}
			set
			{
				if ((this._Reason != value))
				{
					this.OnReasonChanging(value);
					this.SendPropertyChanging();
					this._Reason = value;
					this.SendPropertyChanged("Reason");
					this.OnReasonChanged();
				}
			}
		}
		
		[Column(Name="treshold_value", Storage="_Treshold_value", DbType="Float NOT NULL")]
		public double Treshold_value
		{
			get
			{
				return this._Treshold_value;
			}
			set
			{
				if ((this._Treshold_value != value))
				{
					this.OnTreshold_valueChanging(value);
					this.SendPropertyChanging();
					this._Treshold_value = value;
					this.SendPropertyChanged("Treshold_value");
					this.OnTreshold_valueChanged();
				}
			}
		}
		
		[Column(Name="warning_value", Storage="_Warning_value", DbType="int")]
		public System.Nullable<int> Warning_value
		{
			get
			{
				return this._Warning_value;
			}
			set
			{
				if ((this._Warning_value != value))
				{
					this.OnWarning_valueChanging(value);
					this.SendPropertyChanging();
					this._Warning_value = value;
					this.SendPropertyChanged("Warning_value");
					this.OnWarning_valueChanged();
				}
			}
		}
		
		[Column(Name="caution_value", Storage="_Caution_value", DbType="int")]
		public System.Nullable<int> Caution_value
		{
			get
			{
				return this._Caution_value;
			}
			set
			{
				if ((this._Caution_value != value))
				{
					this.OnCaution_valueChanging(value);
					this.SendPropertyChanging();
					this._Caution_value = value;
					this.SendPropertyChanged("Caution_value");
					this.OnCaution_valueChanged();
				}
			}
		}
		
		[Association(Name="Stopper_Monitoring", Storage="_Monitoring", ThisKey="Stopper_id", OtherKey="Stopper_id")]
		public EntitySet<Monitoring> Monitoring
		{
			get
			{
				return this._Monitoring;
			}
			set
			{
				this._Monitoring.Assign(value);
			}
		}
		
		public event PropertyChangingEventHandler PropertyChanging;
		
		public event PropertyChangedEventHandler PropertyChanged;
		
		protected virtual void SendPropertyChanging()
		{
			if ((this.PropertyChanging != null))
			{
				this.PropertyChanging(this, emptyChangingEventArgs);
			}
		}
		
		protected virtual void SendPropertyChanged(String propertyName)
		{
			if ((this.PropertyChanged != null))
			{
				this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
			}
		}
		
		private void attach_Monitoring(Monitoring entity)
		{
			this.SendPropertyChanging();
			entity.Stopper = this;
		}
		
		private void detach_Monitoring(Monitoring entity)
		{
			this.SendPropertyChanging();
			entity.Stopper = null;
		}
	}
}
#pragma warning restore 1591
