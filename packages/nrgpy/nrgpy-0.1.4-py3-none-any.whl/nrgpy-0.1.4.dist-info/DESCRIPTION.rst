# <img alt="NRGPy" src="https://www.nrgsystems.com/mysite/images/logo.png?v=3" height="40">

NRGPy is the Python package for processing NRG SymphoniePRO Data files

- Website and source: https://github.com/nrgpy/nrgpy
- Support: support@nrgsystems.com

It provides:

- Tools for converting binary ".rld" files to text format
 - using locally installed SymphoniePRO Desktop Software
 - using web api (compatible with Linux!)
- Tools for reading text exports into Pandas dataframes
- Timestamp adjustment (of text files)

***
## Examples:

### Convert a folder of RLD files to Text:
    from nrgpy.convert_rld import local
    date_filter = '2018-10' # filter on any text in the filenames

    text_folder_name = 'text_outputs/'
    fut = local(rld_dir='', out_dir=text_folder_name, filter=date_filter)
    fut.directory()


### Read files
    from nrgpy.sympro_txt import sympro_txt_read

    sympro_dfs = sympro_txt_read()
    sympro_dfs.concat_txt(txt_dir=text_folder_name, output_txt=False)


