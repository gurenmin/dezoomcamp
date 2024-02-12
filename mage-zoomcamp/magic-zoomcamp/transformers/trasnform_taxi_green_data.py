import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def snake_case(str):
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return ''.join(['_'+i.lower() if i.isupper() 
               else i for i in str]).lstrip('_')
    # return str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)

@transformer
def transform(data, *args, **kwargs):
    print("Preprocessing: existing values of VendorId:", set(data['VendorID']))
   
    print("Preprocessing: number of columns need to be renamed:",data.columns.str.contains('(?<=[a-z])(?=[A-Z])',regex=True).sum() )
    
    print("Preprocessing: rows with zero trip_distance:",data['trip_distance'].isin([0]).sum())
    data.columns = (data.columns
                .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                .str.lower()
                    
    )
    data["lpep_pickup_date"] = pd.to_datetime(data["lpep_pickup_datetime"]).dt.date
 
    return data[(data['passenger_count']>0) & (data['trip_distance']>0)]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'passenager count = 0 exists'
    assert output['trip_distance'].isin([0]).sum() == 0, 'trip distance = 0 exists'
    assert 'vendor_id' in output.columns, 'vendor_id not exists'
