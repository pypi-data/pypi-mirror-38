import re
import csv

class etl_pipeline:
    
    """Package for applying ETL operations on input dataFile
    
    Private/Protected Methods
    -------------------------
    _get_delimiters
    _format_rows
    _get_index
    
    Public Methods
    ---------------
    load
    transform
    load_to_csv
    
    output class variables
    --------
    delimiter
    lineterminator
    rejected_rows
    input_rows
    header
    select_list
    """
   
    def _get_delimiters(self):

        """
        returns delimiter and lineterminator of input file.
        It uses Sniffer() method in csv module. 
        This method will be invoked only if delimiter and lineterminator values are not passed to load() method
        """

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(self.__file_obj.readline())
        delimiter = dialect.delimiter
        lineterminator = dialect.lineterminator
        self.__file_obj.seek(0)

        return delimiter,lineterminator


    def _format_rows(self,row_type):

        """
        returns row text as list of columns from the input file using delimiter and lineterminator to split
        """

        formatted_row = re.sub(r'[%s]+' %self.lineterminator,'',self.__line)
        formatted_row = formatted_row.split(self.delimiter)

        if row_type.lower() == 'header':
            for i,name in enumerate(formatted_row):
                j = 0
                if name=='':
                    formatted_row[i] = 'Unknown %s' %str(j+1)
                    j+=1

        return formatted_row

    def _get_index(self):

        """
        generate a list of integers indicating the position of the columns specified in 
        select_list parameter of load() method.Returns integers wrt the header values.
        """

        return [self.header.index(column) for column in self.select_list]
    
    def load(self,dataFile,header=None,select_list=None,skip_rows_with='',delimiter=None,lineterminator=None):
        """
        loads data from dataFile into a python list of lists. Result will contain columns from select_list.
        If select_list is empty complete file is loaded into the list.
        first list in the list is the header information
        """
        self.__file_obj = open(dataFile,"r",encoding="utf-8")
        
        # get file delimiter and lineterminator
        if delimiter is None or lineterminator is None:
            self.delimiter ,self.lineterminator = self._get_delimiters()
        else:
            self.delimiter ,self.lineterminator = delimiter ,lineterminator
      
        # initialise header parameters
        if header is None:
            self.__line = self.__file_obj.readline()
            self.header = self._format_rows(row_type='header')  
        else:
            self.header = header

        # identify the list of columns to be shown in output
        if select_list is None:
            self.select_list = self.header
        else:
            self.select_list = select_list

        # get index details of selected columns
        self._select_index = self._get_index()
        
        # initialise lists for storing header
        self.__result = []
        self.input_rows = []
        self.rejected_rows = []
        
        # store file header
        self.__result.append(self.select_list)
        self.input_rows.append(self.select_list)
        self.rejected_rows.append(self.select_list+['error_desc'])
        
        
        # load formatted row to list
        for self.__line in self.__file_obj.readlines():
            formatted_row = self._format_rows(row_type='data')
            formatted_row = [formatted_row[i].strip() for i in self._select_index]
            if formatted_row == self.select_list:
                continue
            else:
                for value in skip_rows_with:
                    if value in formatted_row:
                        self.rejected_rows.append(formatted_row+['row skipped'])
                        break
                else:
                    self.__result.append(formatted_row)
                    self.input_rows.append(formatted_row.copy())
                    
        #not working. need to use deep copy
        #self.input_rows = list(self.__result)
        #self.input_rows = self.__result.copy()
        self.__file_obj.close()
        
    
    def transform(self,mapping_rule={}):
        
        """
        apply data transform functions defined in the mapping_rule dictionary.
        """ 
        
        # apply transformation             
        for index,column in enumerate(self.select_list):
            
            mapping = mapping_rule.get(column)
            if mapping is None:
                continue
            else:
                for transform in mapping:
                    for i,row in enumerate(self.__result[1:]):
                        
                        try:
                            if type(transform) == dict:
                                self.__result[i+1][index]=transform.get(row[index])
                            elif type(transform) == type:
                                self.__result[i+1][index]=transform(row[index])
                            elif type(transform) == type(lambda x:x):
                                self.__result[i+1][index]=transform(row[index])
                            else:
                                self.__result[i+1][index]=transform(row[index])
                        except Exception as err:
                            self.rejected_rows.append(row+['error at position [{},{}]'.format(i+1,index) + str(err)])
                            raise Exception('Error while applying conversions for line[{},{}]::{} check final entry in rejected_rows output'.format(i+1,index,row))
                    
        
        return self.__result
    
    def load_to_csv(self,filename=None):
        """
        stores the result of transformation function in a csv file
        
        Parameters:
        filename : name of output csv file to store transformed data. if empty creates output.csv in current working directory
        """
        if filename is None:
            filename = 'output.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.__result)