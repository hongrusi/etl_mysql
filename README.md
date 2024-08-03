# etl_mysql

The main purpose of the ETL pipeline is to demonstrate a simple but complete process of fetching data from API and transform it and inject into MySQL database.

- **Extract**: Pulling data from an external API, specifically fetching a list of universities in the United States.
- **Transform**: Manipulating the extracted data using the pandas library. This includes filtering the data to only include universities in California and converting certain list fields into comma-separated strings.
- **Load**: Saving the transformed data into a MySQL database, ensuring the data is stored in a structured and accessible format.
