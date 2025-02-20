/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package dmasemestralka;


import java.io.Serializable;
import java.util.ArrayList;

/**
 *
 * @author já
 */
public class Matrix implements Serializable {

    private int nrRows;
    private int nrColumns;
    private ArrayList<Row> allRows;

    public Matrix(int numberRows, int numberColumns) {
        if (numberRows > 0 & numberColumns > 0) {
            allRows = new ArrayList(numberRows);
            this.nrColumns = numberColumns;
            this.nrRows = numberRows;
            for (int i = 0; i < numberColumns; i++) {
                allRows.add(new Row(numberColumns));
            }
        } else {
            nrColumns = 0;
            nrRows = 0;
            allRows = new ArrayList<Row>(0);
        }
    }

    public Matrix() {
        this(5, 5);
    }

    public Matrix(int square) {
        this(square, square);
    }

    public Matrix(int [][]array){
        allRows = new ArrayList(array.length);
        nrColumns = array[0].length;
        nrRows= array.length;
         for (int i = 0; i < nrRows; i++) {
                allRows.add(new Row(nrColumns));
            }

        for (int i=0;i<array.length;i++){
            for(int j=0;j<array[0].length;j++){
                setField(i,j,(float)array[i][j]);
            }
        }
    }

    public Matrix(float[][] arr) {
        this.nrRows = arr.length;
        this.nrColumns = arr[0].length;
        allRows = new ArrayList<Row>();
        for (int i = 0; i < this.nrRows; i++) {
            allRows.add(new Row(this.nrColumns));
        }
        for (int i = 0; i < this.nrRows; i++) {
            for (int j = 0; j < this.nrColumns; j++) {
                setField(i, j, arr[i][j]);
            }
        }
    }

    public void setField(int rowPos, int colPos, float value) {
        getRow(rowPos).setField(colPos, value);
    }

    public float getField(int rowPos, int colPos) {
        return getRow(rowPos).getField(colPos);
    }

    /**
     * @return the numberRows
     */
    public int getNumberRows() {
        return nrRows;
    }

    /**
     * @return the numberColumns
     */
    public int getNumberColumns() {
        return nrColumns;
    }

    /**
     * @return the allRows
     */
    public ArrayList<Row> getAllRows() {
        return allRows;
    }

    /**
     * @param array the allRows to set
     */
    public void fill(float[][] array) {
        nrRows = array.length;
        nrColumns = array[0].length;
        allRows.clear();
        for (int i = 0; i < nrRows; i++) {
            allRows.add(new Row(nrColumns));
        }
        for (int i = 0; i < nrRows; i++) {
            for (int j = 0; j < nrColumns; j++) {
                setField(i, j, array[i][j]);
            }
        }
    }

    public Matrix add(Matrix matrix) {
        Matrix result = new Matrix(nrRows, nrColumns);
        for (int i = 0; i < this.nrRows; i++) {
            result.setRow(i, allRows.get(i).add(matrix.allRows.get(i)));
        }
        return result;
    }

    public Matrix subtract(Matrix matrix) {
        return add(matrix.multipleByConstant(-1));
    }

    public Matrix transpose() {
        Matrix matrix = new Matrix(nrColumns, nrRows);
        for (int i = 0; i < nrColumns; i++) {
            for (int j = 0; j < nrRows; j++) {
                matrix.allRows.get(i).setField(j, this.getField(j, i));
            }
        }
        return matrix;

    }

    public Matrix multiple(Matrix matrix) {
        Matrix matrix2 = new Matrix(this.nrRows, matrix.nrColumns);
        for (int i = 0; i < this.nrRows; i++) {
            for (int j = 0; j < matrix.nrColumns; j++) {
                matrix2.allRows.get(i).setField(j, this.scalarMultiply(matrix, i, j));
            }
        }
        return matrix2;
    }

    private float scalarMultiply(Matrix matrix, int numRowM1, int numColM2) {
        Matrix matrix2 = matrix.transpose();
        return this.getAllRows().get(numRowM1).scalarMultiply(matrix2.allRows.get(numColM2));
    }

    public void addRow() {
        allRows.add(new Row(nrColumns));
        nrRows++;
    }

    public void addColumn() {
        for (int i = 0; i < getNumberRows(); i++) {
            (allRows.get(i)).addField();
        }
        nrColumns++;
    }

    public Row removeRow() {
        nrRows--;
        if (nrRows == 0) {
            nrColumns = 0;
        }
        return allRows.remove(nrRows);
    }

    public void removeCollumn() {
        for (int i = 0; i < getNumberColumns(); i++) {
            (allRows.get(i)).removeField(nrColumns - 1);
        }
        nrColumns--;
        if (nrColumns == 0) {
            nrRows = 0;
            allRows.clear();
        }
    }

    public String toXML() {
        String S = "<?xml version=\"1.0\" encoding=\"Window UTF-8\"?>\n<Matrix>\n<Description>\n    <rows>" + nrRows + "</rows>\n" +
                "    <columns>" + nrColumns + "</columns>\n</Description>\n";
        for (int i = 0; i < nrRows; i++) {
            S = S + "<row>\n";
            for (int j = 0; j < nrColumns; j++) {
                S = S + "    <cell>" + getField(i, j) + "</cell>\n";
            }
            S = S + "</row>\n";
        }
        S = S + "</Matrix>";
        return S;
    }

    @Override
    public String toString() {
        String S = "";
        for (int i = 0; i < nrRows; i++) {
            for (int j = 0; j < nrColumns; j++) {
                S += getField(i, j)+ "   ";
            }
            S += "\n";
        }
        return S;
    }

    public String toSaveString() {
        String S = "columns=" + getNumberColumns() + "\nrows" + getNumberRows() + "\n";
        for (int i = 0; i < nrRows; i++) {
            for (int j = 0; j < nrColumns; j++) {
                S += ";" + getField(i, j);
            }
            S += "\n";
        }
        return S;
    }

    public void setRow(int index, Row row) {
        getAllRows().remove(index);
        getAllRows().add(index, row);
    }

    public Row getRow(int index) {
        return allRows.get(index);
    }

    public Matrix multipleByConstant(float constant) {
        Matrix result = new Matrix(nrRows, nrColumns);
        for (int i = 0; i < nrRows; i++) {
            result.setRow(i, getRow(i).multiply(constant));
        }
        return result;
    }

 
}
