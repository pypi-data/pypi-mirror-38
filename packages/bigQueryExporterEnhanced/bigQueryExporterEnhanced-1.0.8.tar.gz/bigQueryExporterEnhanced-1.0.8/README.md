# Credit
This repository is forked from
https://github.com/IcarusSO/bigQueryExporter

# Change Log (Compare with original version)
### query_to_local()
- Create a temp table with a random hash on BQ as output table, so that simultaneous execution of the function will not overwrite each other.
- Remove the temp table after the execution. (May also set keep_temp_table=True if you wish to keep them).

# bigQueryExporter
Export query data from google bigquery to local machine

#### Installation
    pip install bigQueryExporterEnhanced
    
#### Prepare for the connection
    from bigQueryExport import BigQueryExporter
    bigQueryExporter = BigQueryExporter(project_name, dataset_name, bucket_name)   

#### Query To Table
    bigQueryExporter.query_to_table(query, job_name, dataset_name)
    
#### Table To GS
    bigQueryExporter.table_to_gs(destination_table, job_name)
    
#### GS To Local
    bigQueryExporter.gs_to_local(bucket, job_name, data_dir_path)
    
#### Query To GS (Query to Table + Table to GS)
    bigQueryExporter.query_to_gs(query, job_name)

#### Query To Local (Query to Table + Table to GS + GS to Local)
    export_path = bigQueryExporter.query_to_local(query)
    
    # or with the options
    export_path = bigQueryExporter.query_to_local(query, 
                                                  job_name='simple_query', 
                                                  data_dir_path='out/',
                                                  keep_temp_table=False,
                                                  overwrite_output_folder=True)
    
#### Requirement
- Your server/ local machine should have the right to access the project
- Right should be granted following the insturction on [Google SDK](https://cloud.google.com/sdk/docs/)
- Execute the following command

    gcloud auth application-default login
