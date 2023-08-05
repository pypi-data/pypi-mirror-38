import sys
sys.path.append("bigQueryExporter")

from BigQueryExporterEnhanced import BigQueryExporterEnhanced

bq_exporter = BigQueryExporterEnhanced("bigquery-161507", "dna", key_file_path="/Users/jason.tsang/anaconda3/lib/python3.6/site-packages/settings/certs/ds_bigquery_credential.json")

export_file_path = bq_exporter.query_to_local("select * from `dna.bxid_info`")
