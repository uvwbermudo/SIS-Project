#UREL VAN WILLIAM BERMUDO BSCS, 2ND YEAR, CCC151, SIS HOMEWORK

from distutils import core
from importlib.resources import path
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView, QErrorMessage, QPushButton, QHBoxLayout, QMessageBox
from PyQt5 import uic, QtCore
import bermudosis as bm
import pandas as pd
import os

# credits https://www.reddit.com/r/learnpython/comments/69vm4t/pyqt5_and_high_resolution_monitors/ 
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) 

class EDITform(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/editwindow.ui', self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')
        self.doneEdit.pressed.connect(self.editData)
        self.chosenRow = ''
        self.fromSearch = False


    def editData(self):
        row = self.chosenRow            
        reply = QMessageBox.question(self, 'Confirmation', 'Save edit changes?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            pass
        else:
            self.close()
            return

        idNumber = self.idField.text()
        if (bm.searchStudent(idNumber, bm.mainfile, self.chosenRow) != -1):
            self.error_dialog.showMessage('ID Number already in use by another student on this class!')
            return
            
        if (self.checkIDformat(idNumber) == False):
            self.error_dialog.showMessage('Invalid ID Number format!')
            return

        fullName = self.nameField.text()
        if (fullName == ''):
            self.error_dialog.showMessage('Name field cannot be blank!')
            return

        course = self.courseField.text()
        if (course == ''):
            self.error_dialog.showMessage('Course field cannot be blank!')
            return

        year = self.yearField.text()
        if (self.checkYear(year) == False):
            self.error_dialog.showMessage('Please input a valid year level!')
            return
        gender = self.genderField.currentText()
        bm.editstudent(idNumber,fullName.title(),course.upper(),year,gender,bm.mainfile,self.chosenRow)
        self.close()   
        mygui.refresh()

    def checkIDformat(self, idNumber):
        if len(idNumber)!= 9:
            return False
        for i in range(len(idNumber)):
            if i != 4:
                try:
                    int(idNumber[i])
                except:
                    return False
            if i == 4:
                if idNumber[i] != '-':
                    return False
        return True
    def checkYear(self,year):
        try:
            int(year)
            str(year)
        except:
            return False


class ADDform(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'{sys.path[0]}/addwindow.ui', self)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')
        self.doneAdd.pressed.connect(self.getData)
    

    def getData(self):
        idNumber = self.idField.text()
        if (bm.searchStudent(idNumber, bm.mainfile) != -1):
            self.error_dialog.showMessage('ID Number already in use by another student on this class!')
            return
            
        if (self.checkIDformat(idNumber) == False):
            self.error_dialog.showMessage('Invalid ID Number format!')
            return

        fullName = self.nameField.text()
        if (fullName == ''):
            self.error_dialog.showMessage('Name field cannot be blank!')
            return

        course = self.courseField.text()
        if (course == ''):
            self.error_dialog.showMessage('Course field cannot be blank!')
            return

        year = self.yearField.text()
        if (self.checkYear(year) == False):
            self.error_dialog.showMessage('Please input a valid year level!')
            return
        gender = self.genderField.currentText()
        bm.addStudent(idNumber,fullName.title(),course.upper(),year,gender,bm.mainfile)
        self.doneAdd.setEnabled(False)
        self.close()
        self.idField.clear()
        self.nameField.clear()
        self.courseField.clear()
        self.yearField.clear()
        mygui.refresh()
    
    def checkIDformat(self, idNumber):
        if len(idNumber)!= 9:
            return False
        for i in range(len(idNumber)):
            if i != 4:
                try:
                    int(idNumber[i])
                except:
                    return False
            if( (i == 4) and (idNumber[i] != '-')):
                    return False
        return True

    def checkYear(self,year):
        try:
            int(year)
            str(year)
        except:
            return False





class SISgui(QMainWindow):  


    def __init__(self):
        bm.mainfile = ''
        super().__init__()
        bm.makeDefaultFile()                    # makes a csv file only for testing, can be removed 
        uic.loadUi(f'{sys.path[0]}/mainwindow.ui', self)
        self.addButton.pressed.connect(self.openAddWindow)        #connecting buttons to function
        self.searchButton.pressed.connect(self.findStudent)                         
        self.openButton.pressed.connect(self.openCSV)
        self.showButton.pressed.connect(self.refresh)
        self.createButton.pressed.connect(self.createFile)
        self.miscButton.pressed.connect(self.deleteClass)
        self.filename = ''              #filename currently opened

        
        self.createButton.pressed.connect(self.openAddWindow)
        self.headerLabels =['ID Number','Full Name','Course','Year Level','Gender','Action']   
        self.all_data = pd.DataFrame(columns = self.headerLabels[:-1])                        # this attribute should be used for the pandas dataframe
        self.displayData(self.all_data)
        self.fromSearch = False                 # will be used to check if currently displayed student is from search
        self.searchedRow = None
        self.tempFrame = pd.DataFrame()         #will be used to display temporary dataframe when searching
        
        # error message object
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowTitle('Error')

        #adds student and edit student window initialize
        self.window2 = ADDform()
        self.window3 = EDITform()


    def deleteClass(self):
        if(self.checkFileExists() == False):
            return
        reply = QMessageBox.question(self, 'Delete this class', f'Are you sure you want to delete this class: "{self.filename}"? ',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            os.remove(bm.mainfile)
            self.clear_table()
            self.setWindowTitle(f'Bermudo\'s Student Information System')
            self.pathLabel.setText(f'Current file:')


        else:   
            pass



    def createFile(self):
        try:
            path = QFileDialog.getSaveFileName(self, 'Save CSV File', os.getenv('HOME'), 'CSV(*.csv)' )[0]
        except:
            print(path)
        columns = ','.join(self.headerLabels[:-1]) + '\n'
        if (path == ''):
            return

        with open(path, 'w') as f:
            f.write(columns)
        bm.mainfile = path
        self.all_data = pd.read_csv(path)
        self.displayData(self.all_data)
        self.filename = os.path.basename(bm.mainfile)
        self.setWindowTitle(f'Bermudo\'s Student Information System - {self.filename}')
        self.pathLabel.setText(f'Current file: {bm.mainfile}')



    def openEditWindow(self,row):
        int(row)
        if (self.checkFileExists() == False):
            return
        self.window3.chosenRow = row
        self.window3.doneEdit.setEnabled(True) # preventing double clicking
        self.window3.idField.setText(self.all_data.loc[row].at['ID Number'])
        self.window3.nameField.setText(self.all_data.loc[row].at['Full Name'])
        self.window3.courseField.setText(self.all_data.loc[row].at['Course'])
        self.window3.yearField.setText(str(self.all_data.loc[row].at['Year Level']))
        self.window3.genderField.setCurrentText(self.all_data.loc[row].at['Gender'])

        self.window3.show()



    def openAddWindow(self):
        if (self.checkFileExists() == False):
            return
        self.window2.doneAdd.setEnabled(True) # preventing double clicking
        self.window2.setWindowTitle(f'Add Student Form - {self.filename}')
        self.window2.show()


        

        # method for making the delete and edit buttons that will be used for each row
    def makeButtons(self, row):                          # yoinked from https://stackoverflow.com/questions/60396536/pyqt5-setcellwidget-on-qtablewidget-slows-down-ui
        self.editButton = QPushButton('Edit')
        self.editButton.pressed.connect(lambda:self.openEditWindow(row))

        self.deleteStudentButton = QPushButton('Delete')
        self.deleteStudentButton.pressed.connect(lambda:self.deleteStudent(row))

        self.actionLayout = QHBoxLayout()
        self.actionLayout.addWidget(self.deleteStudentButton,5)
        self.actionLayout.addWidget(self.editButton,5)
        self.actionWidget = QWidget()
        self.actionWidget.setLayout(self.actionLayout)
        return self.actionWidget


    def deleteStudent(self, row):
        if(self.checkFileExists() == False):
            return
        reply = QMessageBox.question(self, self.all_data.loc[row].at['Full Name'], 'Are you sure you want to delete this student?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.all_data = bm.deletestudent(row,bm.mainfile)
            self.refresh()
        else:
            pass


            
    def openCSV(self):                          #yoinked the code from https://www.youtube.com/watch?v=HDjc3w1W9oA
        try:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
        except:
            print(path)
            
        if (path != ''):
            bm.mainfile = path
        else:
            path = bm.mainfile


        if(self.checkCSVformat() == False):
            bm.mainfile = ''
            return

        print(f'Current path is {bm.mainfile}')
        self.filename = os.path.basename(bm.mainfile)
        self.pathLabel.setText(f'Current file: {bm.mainfile}')
        self.displayData(self.all_data)
        self.setWindowTitle(f'Bermudo\'s Student Information System - {self.filename}')



    def checkCSVformat(self):
        columns = ['ID Number', 'Full Name', 'Course', 'Year Level', 'Gender']
        if len(self.all_data.columns) == 5:
            pass
        else:
            self.error_dialog.showMessage('Invalid CSV Format for SIS')
            return False


        for col in self.all_data.columns:
            if col in columns:
                pass
            else:
                self.error_dialog.showMessage('Invalid CSV Format for SIS')
                return False



    def clear_table(self):
        while(self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)



    def checkFileExists(self):
        path = bm.mainfile
        if(path == ''):
            self.error_dialog.showMessage('Error! No file selected.')
            return False

        elif(os.path.exists(path) == False):
            self.error_dialog.showMessage('Error! File not found. (File has been deleted or modified.) Please open or create a CSV file first.')
            return False
        return True

        
            
    def refresh(self):
        self.fromSearch = False
        if(self.checkFileExists() == False):
            return
        self.clear_table
        self.all_data = pd.read_csv(bm.mainfile)
        self.displayData(self.all_data)
        


    def displayData(self, dataframe):                           #yoinked the code from https://www.youtube.com/watch?v=HDjc3w1W9oA
        hheader = self.tableWidget.horizontalHeader()           #stole this from https://www.tutorialexample.com/pyqt-table-set-adaptive-width-to-fit-resized-window-a-beginner-guide-pyqt-tutorial/
        hheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader = self.tableWidget.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.Fixed)        # row resize: https://stackoverflow.com/questions/19304653/how-to-set-row-height-of-qtableview
        vheader.setDefaultSectionSize(40)

        numColumn = len(dataframe.columns)+1
        numRows = len(dataframe.index) 
        self.tableWidget.setColumnCount(numColumn)
        self.tableWidget.setRowCount(numRows)
        self.tableWidget.setHorizontalHeaderLabels(self.headerLabels)
        

        lastColumn = len(dataframe.columns)-1
        for i in range(numRows):
            for j in range(len(dataframe.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(dataframe.iat[i, j])))
            if self.fromSearch:
                actionWidget = self.makeButtons(self.searchedRow)
            else:
                actionWidget = self.makeButtons(i)
            self.tableWidget.setCellWidget(i, 5, actionWidget)
            


    def findStudent(self):
        if(self.checkFileExists() == False):
            return
        try:
            idnumber = self.searchBar.text()
            row = bm.searchStudent(idnumber,bm.mainfile)
            if (row == -1):
                self.error_dialog.showMessage('Student does not exist.')
                self.searchBar.clear()
                return False
            fullName = str(self.all_data.loc[row].at['Full Name'])
            course = str(self.all_data.loc[row].at['Course'])
            year = str(self.all_data.loc[row].at['Year Level'])
            gender = str(self.all_data.loc[row].at['Gender'])
            data = {'ID Number':[str(idnumber)],
                    'Full Name':[str(fullName)],
                    'Course':[str(course)],
                    'Year Level':[str(year)],
                    'Gender':[str(gender)]
                }
                
            self.tempFrame = pd.DataFrame(data)
            self.fromSearch = True
            self.searchedRow = row
            self.displayData(self.tempFrame)


        except Exception:
            self.error_dialog.showMessage('Invalid ID Number format. e.g.(2020-1971)')
            self.searchBar.clear()
        
        return True
      


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mygui = SISgui()
    mygui.show()

    try:
        sys.exit(app.exec_())
    except (SystemExit):
        print("Closing window...")






