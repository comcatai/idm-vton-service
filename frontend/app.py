import streamlit as st
import requests
import base64
from PIL import Image
import io
import time
import os

# Constants
RUNPOD_ENDPOINT = "https://api.runpod.ai/v2/tzf4ssrs23sj1r/run"
API_KEY = "rpa_J84C3C24H9CX8N66FY7PP5KABDNGL9JTMKTE79VDl6bmxh"

def image_to_base64(image):
    if isinstance(image, Image.Image):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    else:
        return base64.b64encode(image.read()).decode('utf-8')

def try_on_clothing(person_image, cloth_image):
    # Convert images to base64
    person_base64 = image_to_base64(person_image)
    cloth_base64 = image_to_base64(cloth_image)
    
    # Prepare the request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "person_image": person_base64,
            "cloth_image": cloth_base64
        }
    }
    
    # Make the request
    with st.spinner('Processing virtual try-on...'):
        st.write("Sending request to RunPod...")
        response = requests.post(RUNPOD_ENDPOINT, json=payload, headers=headers)
        st.write(f"Response Status Code: {response.status_code}")
        st.write(f"Response Headers: {dict(response.headers)}")
        
        try:
            if response.status_code == 200:
                data = response.json()
                st.write(f"Initial Response Data: {data}")
                
                # Check if it's async (webhook) or sync response
                if "id" in data:
                    # Async response - need to check status
                    st.write(f"Got task ID: {data['id']}")
                    return check_status(data["id"])
                else:
                    # Sync response
                    return data
            else:
                st.error(f"Error: {response.status_code}")
                st.error(f"Error Response: {response.text}")
                return None
        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            st.error(f"Raw Response: {response.text}")
            return None

def check_status(task_id):
    status_url = f"https://api.runpod.ai/v2/tzf4ssrs23sj1r/status/{task_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    start_time = time.time()
    max_retries = 60  # 5 minutes timeout
    retries = 0
    
    while retries < max_retries:
        try:
            st.write(f"Checking status attempt {retries + 1}...")
            response = requests.get(status_url, headers=headers)
            st.write(f"Status check response code: {response.status_code}")
            
            try:
                status_data = response.json()
                st.write(f"Status Response: {status_data}")
                
                if status_data["status"] == "COMPLETED":
                    progress_bar.progress(100)
                    status_text.text("Processing complete!")
                    return status_data["output"]
                elif status_data["status"] == "FAILED":
                    progress_bar.progress(100)
                    st.error(f"Task failed: {status_data.get('error', 'Unknown error')}")
                    if "logs" in status_data:
                        st.error(f"Task logs: {status_data['logs']}")
                    return None
                elif status_data["status"] == "IN_QUEUE":
                    status_text.text("Request in queue...")
                elif status_data["status"] == "IN_PROGRESS":
                    status_text.text("Processing your images...")
                else:
                    status_text.text(f"Status: {status_data['status']}")
            except Exception as e:
                st.error(f"Error parsing status JSON: {str(e)}")
                st.write(f"Raw status response: {response.text}")
            
            # Update progress (simulated)
            elapsed_time = time.time() - start_time
            progress = min(90, elapsed_time * 5)  # Max 90% until complete
            progress_bar.progress(int(progress))
            
            retries += 1
            time.sleep(5)
        except Exception as e:
            st.error(f"Error checking status: {str(e)}")
            return None
    
    st.error("Request timed out after 5 minutes")
    return None

def main():
    st.title("IDM-VTON Virtual Try-On")
    st.write("Upload a person image and a clothing image to see how the clothing looks on the person!")

    # File uploaders
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Person Image")
        person_image = st.file_uploader("Upload person image", type=['jpg', 'jpeg', 'png'])
        if person_image:
            st.image(person_image, caption="Person Image", use_column_width=True)
    
    with col2:
        st.subheader("Clothing Image")
        cloth_image = st.file_uploader("Upload clothing image", type=['jpg', 'jpeg', 'png'])
        if cloth_image:
            st.image(cloth_image, caption="Clothing Image", use_column_width=True)

    # Process button
    if st.button("Try On Clothing") and person_image and cloth_image:
        result = try_on_clothing(person_image, cloth_image)
        
        if result and "generated_image" in result:
            # Convert base64 to image and display
            generated_image = Image.open(io.BytesIO(base64.b64decode(result["generated_image"])))
            st.subheader("Result")
            st.image(generated_image, caption="Virtual Try-On Result", use_column_width=True)
            
            # Add download button
            buffered = io.BytesIO()
            generated_image.save(buffered, format="JPEG")
            st.download_button(
                label="Download Result",
                data=buffered.getvalue(),
                file_name="virtual_tryon_result.jpg",
                mime="image/jpeg"
            )
    
    st.markdown("---")
    st.markdown("""
    ### Instructions:
    1. Upload a full-body photo of a person
    2. Upload a clothing image (preferably on white background)
    3. Click 'Try On Clothing' to see the result
    """)

if __name__ == "__main__":
    main()
