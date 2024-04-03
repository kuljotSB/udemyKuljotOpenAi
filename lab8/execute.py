#importing important libraries and utilities
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

form_endpoint="YOUR_FORM_RECOGNIZER_ENDPOINT"
form_key="YOUR_FORM_RECOGNIZER_KEY"

oai_key="YOUR_AZURE_OAI_KEY"
oai_endpoint="YOUR_AZURE_OAI_ENDPOINT_HERE"
model_name="YOUR_AZURE_OAI_MODEL_HERE"

client = AzureOpenAI(
    azure_endpoint=oai_endpoint,
    api_key=oai_key,
    api_version="2024-02-15-preview"
)

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return "," .join("Page #{}:{}".format(region.page_number, format_polygon(region.polygon)) for region in bounding_regions)

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ",".join(["[{},{}]".format(p.x,p.y) for p in polygon])

document_url="https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-invoice.pdf"
document_analysis_client=DocumentAnalysisClient(endpoint=form_endpoint, credential=AzureKeyCredential(form_key))
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-invoice", document_url)
invoices=poller.result()


for idx,invoice in enumerate(invoices.documents):
    vendor_name=invoice.fields.get("VendorName")
    vendor_name_value=vendor_name.value
    
    vendor_address = invoice.fields.get("VendorAddress")
    vendor_address_value=vendor_address.value
    
    invoice_date=invoice.fields.get("InvoiceDate")
    invoice_date_value = invoice_date.value
    
    subtotal=invoice.fields.get("SubTotal")
    subtotal_value=subtotal.value
    
system_content="you are an AI assistant"

user_content = "You have been provided the details of an invoice. generate a csv file based upon the following details given to you \n"  +"vendor name: " + str(vendor_name_value) + "\n" + "vendor address: " + str(vendor_address_value) + "\n" + "invoice date: " + str(invoice_date_value) +"\n" + "subtotal: " + str(subtotal_value)

messages = [
    {"role":"system", "content":system_content},
    {"role":"user", "content":user_content}
]

response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=0.7
)

print(response.choices[0].message.content)



    
