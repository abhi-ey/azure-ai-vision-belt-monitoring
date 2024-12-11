# Azure AI Vision for Conveyor Belt Carryback Detection

This repository provides tools and code to monitor conveyor belt images using Azure AI Vision. The goal is to detect signs of carryback and upload results to a visualization dashboard like Streamlit for monitoring and analysis.

## Features

- **Image Monitoring**: Analyze conveyor belt images using Azure AI Vision.
- **Carryback Detection**: Identify and flag images with potential carryback issues.
- **Visualization Dashboard**: Display results using a Streamlit dashboard for easy monitoring.
- **Scalable Design**: Easily integrate with other Azure services and extend functionality.

## Prerequisites

1. **Azure Subscription**: Access to Azure AI Vision and related services.
2. **Python 3.8+**: Ensure Python is installed on your system.
3. **Streamlit**: For dashboard visualization. Install it using:
   ```bash
   pip install streamlit
   ```
4. **Azure SDKs**: Install required Azure libraries:
   ```bash
   pip install azure-cognitiveservices-vision-customvision azure-storage-blob
   ```
5. **Image Dataset**: A collection of conveyor belt images to analyze.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/azure-ai-carryback.git
   cd azure-ai-carryback
   ```

2. Set up Azure AI Vision:
   - Create an Azure AI Vision resource in your Azure portal.
   - Note the **Endpoint** and **Key** for API access.

3. Configure your environment:
   - Create a `.env` file in the project root with the following variables:
     ```env
     AZURE_VISION_ENDPOINT=<your-azure-endpoint>
     AZURE_VISION_KEY=<your-azure-key>
     ```

4. Prepare the Streamlit dashboard:
   - Run the dashboard:
     ```bash
     streamlit run app.py
     ```

## Usage

1. Upload images of conveyor belts to the input directory or specify a data source.
2. Run the image analysis script:
   ```bash
   python analyze_images.py
   ```
3. View results in the Streamlit dashboard.

## Project Structure

- **`analyze_images.py`**: Script for analyzing images with Azure AI Vision.
- **`app.py`**: Streamlit application for visualizing results.
- **`utils/`**: Utility functions for image preprocessing and API interactions.
- **`data/`**: Directory for input images and output results.

## Contributing

We welcome contributions! Please:

1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [your-email@example.com].

