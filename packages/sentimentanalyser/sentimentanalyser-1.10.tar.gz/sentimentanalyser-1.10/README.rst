sentimentanalyser

Following are the steps to be followed to use this package

install
$ pip install sentimentanalyser

To train your dataset


>import sentimentanalyser
>from sentimentanalyser import train
>filePath="path_to_your_csv_file"
>outputDir="path_where_you_want_your_outputs_to_reside"
>trainObj=train.Train()
>trainObj.train_file_model(filePath,outputDir)

Output folder will contain the vectorlib and model pkl files

>To test your dataset
>testText=""
>test_file_name="path_to_your_unlabelled_csv_file"
>test_reference_file="path_to_your_pkl_files"
>outputDir="path_to_ouput_folder"
>from sentimentanalyser import test
>testObj=test.TestData()
>testedDataFrame=testObj.test_model(testText,test_file_name,test_reference_file,outputDir)
