https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=your_layer_name&outputFormat=application/json



Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point


https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point&outputFormat=application/json


To retrieve GeoJSON objects from the specified Web Feature Service (WFS) endpoint, you can construct a `GetFeature` request with the `outputFormat` parameter set to `application/json`. Here's how you can do it:

1. **Identify the Layer Name**: First, determine the exact name of the layer you wish to access. You can find this information in the WFS capabilities document available at:

   ```
   https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?request=GetCapabilities&service=WFS
   ```


   Open this URL in your browser and look for the `<Name>` tags within the `<FeatureTypeList>` section to identify available layer names.

2. **Construct the GetFeature Request**: Once you have the layer name, you can request its features in GeoJSON format by constructing a URL like the following:

   ```
   https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=your_layer_name&outputFormat=application/json
   ```


   Replace `your_layer_name` with the actual name of the layer you're interested in.

3. **Execute the Request**: Paste the constructed URL into your web browser or use a tool like `curl` to execute the request. The server should respond with the features in GeoJSON format.

For example, if the layer name is `Kulturhistoriska_lamningar:historical_sites`, your request URL would be:


```
https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:historical_sites&outputFormat=application/json
```


This approach leverages GeoServer's support for GeoJSON output via WFS, as detailed in the GeoServer documentation. citeturn0search0

Ensure that the layer name is correct and that the server supports the GeoJSON output format. If you encounter any issues, refer to the GeoServer WFS documentation or contact the service provider for assistance. 




Great questions! You can filter WFS queries using the **Filter Encoding (CQL, OGC Filters, or bounding box queries)** to fetch only objects in a particular area or with specific attributes. Below are different approaches to achieve this:

---

### 1️⃣ **Fetch Only Objects in a Particular Area**
You can use a **bounding box (BBOX) filter** to fetch features within a specific area.

#### Example: Fetch objects within a bounding box  
```plaintext
https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?
service=WFS&
version=1.0.0&
request=GetFeature&
typeName=your_layer_name&
outputFormat=application/json&
bbox=minx,miny,maxx,maxy,EPSG:4326
```
Replace:
- `your_layer_name` with the actual name of the layer
- `minx, miny, maxx, maxy` with the coordinates of the bounding box
- `EPSG:4326` with the correct projection if needed (WGS 84 in this case)

---

### 2️⃣ **Fetch Objects with Particular Attributes**
You can use **CQL (Common Query Language) filters** to query objects with specific attributes.

#### Example: Fetch objects where attribute `status = 'active'`
```plaintext
https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?
service=WFS&
version=1.0.0&
request=GetFeature&
typeName=your_layer_name&
outputFormat=application/json&
CQL_FILTER=status='active'
```

You can also filter numerical values, for example:
- **Fetch objects where `year > 1900`**  
  ```
  CQL_FILTER=year>1900
  ```

- **Fetch objects where `category = 'church'`**  
  ```
  CQL_FILTER=category='church'
  ```

---

### 3️⃣ **Combine Both (Area + Attribute Filters)**
You can **combine** a `BBOX` filter with an **attribute filter** using CQL.

#### Example: Fetch objects within a bounding box AND with `status='active'`
```plaintext
https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?
service=WFS&
version=1.0.0&
request=GetFeature&
typeName=your_layer_name&
outputFormat=application/json&
CQL_FILTER=BBOX(geometry, minx, miny, maxx, maxy) AND status='active'
```

#### Example: Fetch objects with `year > 1900` inside a bounding box
```plaintext
https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?
service=WFS&
version=1.0.0&
request=GetFeature&
typeName=your_layer_name&
outputFormat=application/json&
CQL_FILTER=BBOX(geometry, minx, miny, maxx, maxy) AND year>1900
```

---

### 🛠️ **Alternative: Use OGC Filters (XML-Based)**
If the server does not support CQL, you can use OGC XML filters. This is more complex but more flexible.

Let me know if you need an example of that! 🚀


Yes! You can retrieve unique values from an attribute using a **WFS GetFeature request** combined with filtering and post-processing. However, WFS itself does not have a direct "DISTINCT" or "GROUP BY" function like SQL. Instead, you need to retrieve all values and extract unique ones on the client side.  

### 1️⃣ **Fetch All Values of an Attribute**
You can retrieve features and then extract unique values from a specific attribute (e.g., `category`) in your script or GIS tool.

#### Example: Get All Features with a Specific Attribute
```plaintext
https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?
service=WFS&
version=1.0.0&
request=GetFeature&
typeName=your_layer_name&
outputFormat=application/json&
propertyName=category
```
🔹 **`propertyName=category`** ensures that only the `category` field is returned, reducing data size.

---

### 2️⃣ **Post-Process to Extract Unique Values**
Since WFS does not return distinct values, you can process the response in **Python, JavaScript, or GIS tools**.

#### **Python Example**
```python
import requests
import json

url = "https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=your_layer_name&outputFormat=application/json&propertyName=category"

response = requests.get(url)
data = response.json()

# Extract unique values
unique_categories = set(feature["properties"]["category"] for feature in data["features"])
print(unique_categories)
```

---

### 3️⃣ **Alternative: Use CQL to Filter on Unique Values**
If you already know some values and want to confirm their existence, you can use:
```plaintext
CQL_FILTER=category IN ('church', 'castle', 'bridge')
```
But this requires you to know possible values beforehand.

---

### 4️⃣ **PostGIS / GeoServer SQL View (Advanced)**
If you have access to GeoServer's backend (PostGIS database), you can create a **SQL View**:
```sql
SELECT DISTINCT category FROM your_table;
```
Then expose this as a new WFS layer.

---

### 📌 **Summary**
- WFS does not have a built-in "DISTINCT" function.
- Use `propertyName=your_attribute` to limit the data.
- Extract unique values on the client side using Python, JavaScript, or GIS software.
- If you control the server, use a SQL View with `DISTINCT`.

Would you like an example for a different tool like JavaScript or QGIS? 🚀


That sounds great! If you're using JavaScript, you can easily fetch and extract unique values like this:  

### **JavaScript Example**
```javascript
fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=your_layer_name&outputFormat=application/json&propertyName=category")
  .then(response => response.json())
  .then(data => {
    const uniqueCategories = [...new Set(data.features.map(f => f.properties.category))];
    console.log(uniqueCategories);
  })
  .catch(error => console.error("Error fetching data:", error));
```

### **Explanation**
1. Fetches the WFS data with only the `category` attribute.
2. Extracts all `category` values from features.
3. Uses `new Set()` to get unique values.
4. Logs the result.

🚀 Now you can integrate this into a web app or a map! Let me know if you need further tweaks. 😃


https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point&outputFormat=application/json

fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=kulturhistoriska_lamningar_point&outputFormat=application/json&propertyName=lan")
  .then(response => response.json())
  .then(data => {
    const uniqueCategories = [...new Set(data.features.map(f => f.properties.category))];
    console.log(uniqueCategories);
  })
  .catch(error => console.error("Error fetching data:", error));

fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=kulturhistoriska_lamningar_point&outputFormat=application/json")
  .then(response => response.json())


  fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point&outputFormat=application/json")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Error fetching data:", error));


fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point&outputFormat=application/json")
  .then(response => response.json())
  .then(data => console.log(data))
  .then(data => {
    const uniqueCategories = [...new Set(data.features.map(f => f.properties.category))];
    console.log(uniqueCategories);
  })
  .catch(error => console.error("Error fetching data:", error));



fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point&outputFormat=application/json")
  .then(response => response.text())  // Read as text first
  .then(data => {
    console.log("Raw response:", data);  // Log full response
    return JSON.parse(data);  // Try parsing JSON
  })
  .then(data => console.log("Parsed JSON:", data))
  .catch(error => console.error("Error fetching data:", error));


fetch("https://inspire-raa.metria.se/geoserver/Kulturhistoriska_lamningar/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=Kulturhistoriska_lamningar:kulturhistoriska_lamningar_point&outputFormat=application/json")
  .then(response => response.json())
  .then(data => {
    console.log("Data received:", data);  // Inspect the entire data object

    // Log the first feature's properties for inspection
    console.log("First feature properties:", data.features[0].properties);

    // If 'category' doesn't exist, you can change it to another valid property like 'lamningtyp' or 'kommun'
    const uniqueCategories = [...new Set(data.features.map(f => f.properties.lamningtyp))];
    console.log("Unique lamning types:", uniqueCategories);
  })
  .catch(error => console.error("Error fetching data:", error));