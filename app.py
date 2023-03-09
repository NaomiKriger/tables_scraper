import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def app_index():
    return {"message": "Welcome to the app sources and statuses server!"}


sources = {"wabetainfo": "https://wabetainfo.com/updates/?filter=1"}
versions_and_sources = {}


@app.route("/back_fill_versions/<source_name>", methods=['GET'])
def back_fill_versions(source_name: str) -> dict:
    if source_name in sources:
        url = sources[source_name]
    else:
        return {}

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    tables = soup.find_all('table', class_='styled-table')

    if source_name in versions_and_sources:
        dict_to_update = {source_name: versions_and_sources[source_name]}
    else:
        dict_to_update = {source_name: {}}

    for table in tables:
        current_table = pd.read_html(str(table))[0][['SOURCE', 'VERSION']]
        for index, row in current_table.iterrows():
            if row.VERSION not in dict_to_update[source_name]:
                dict_to_update[source_name].update({row.VERSION: {'source': row.SOURCE, 'tested': False}})
    versions_and_sources.update(dict_to_update)
    return versions_and_sources


@app.route("/versions_and_sources", methods=['GET'])
def get_versions_and_sources():
    return versions_and_sources


@app.route("/versions/<source_name>", methods=['GET'])
def get_versions_of_source(source_name: str):
    if source_name in versions_and_sources:
        return {source_name: versions_and_sources[source_name]}


@app.route("/versions/<source_name>/<source_status>", methods=['GET'])
def get_testflight_versions(source_name: str, source_status: str) -> dict:
    versions = get_versions_of_source(source_name)
    testflight_versions = {}
    for key, val in versions.get(source_name).items():
        if val.get('source') == source_status.upper():
            testflight_versions[key] = val
    return {f"{source_name}_{source_status}": testflight_versions}


@app.route("/versions/<source_name>/update", methods=['POST'])
def update_version(source_name: str) -> dict:
    content = request.json
    version_to_update = content.get("version_to_update")
    tested_value = content.get("tested_value")

    versions = get_versions_of_source(source_name)
    if version_to_update in versions.get(source_name):
        versions[source_name][version_to_update]['tested'] = tested_value
        return {version_to_update: versions[source_name][version_to_update]}
    else:
        return {}


@app.route("/versions/<source_name>/delete", methods=['DELETE'])
def delete_version(source_name: str) -> str:
    content = request.json
    versions = get_versions_of_source(source_name)
    version_to_delete = content.get("version_to_delete")
    if version_to_delete not in versions.get(source_name):
        return f'version {version_to_delete} not found'
    else:
        del versions[source_name][version_to_delete]
        return f'version {version_to_delete} deleted'


app.run(host="0.0.0.0", port=5000, debug=True)
