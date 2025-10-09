# Looker Agent with ADK and MCP Toolbox

This repository contains the necessary steps to implement and deploy a Looker agent using the ADK (Agent Development Kit) and MCP (Model Context Protocol) Toolbox.

-----

## MCP Toolbox for Looker Implementation

First, you need to set up the MCP Toolbox server.

1.  **Navigate to the `mcp-toolbox` directory and replace the contents in the .env file with your variables**:

    ```shell
    BASE_URL=your_looker_instance_url
    LOOKER_CLIENT_ID=your_client_id
    LOOKER_CLIENT_SECRET=your_client_secret
    ```
2.  **Load your variables from the .env file into your terminal session as environment variables.**:

    ```shell
    export $(grep -v '^#' .env | xargs)
    ```

3.  **Start the server**:

    ```shell
    ./toolbox --tools-file "tools.yaml"
    ```

6.  **To test it locally with an interactive UI**:

    ```shell
    ./toolbox --ui
    ```

-----

## MCP Toolbox with ADK

Next, create the agent and connect it to your tools.

1.  **Navigate to the `my-agents` directory, set up a virtual environment, and activate it**:

    ```shell
    cd my-agents
    python -m venv .venv
    source .venv/bin/activate
    ```
    
2.  **Replace the contents in the .env file with your variables**:

    ```shell
    GOOGLE_GENAI_USE_VERTEXAI=1
    GOOGLE_CLOUD_PROJECT=your_google_cloud_project_id
    GOOGLE_CLOUD_LOCATION=us-central1
    LOOKER_CLIENT_ID=your_looker_client_id
    LOOKER_CLIENT_SECRET=your_looker_client_secret
    LOOKER_BASE_URL=your_looker_instance_url
    ```

3.  **Install the ADK and MCP Toolbox packages**:

    ```shell
    pip install google-adk toolbox-core
    ```

4.  **Test your agent locally**. This command will return a URL for testing.

    ```shell
    adk web
    ```

    **Note**: The MCP server must be running for the agent to access the tools.

-----

## Deploying the Agent to Cloud Run

Finally, deploy the MCP Toolbox and the agent to Cloud Run.

### Deploy the MCP Toolbox

1.  **Navigate to your `mcp-toolbox` directory, define your `PROJECT_ID`, and enable the necessary services**:

    ```shell
    export PROJECT_ID="YOUR_GOOGLE_CLOUD_PROJECT_ID"
    gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com
    ```

2.  **Create a service account**:

    ```shell
    gcloud iam service-accounts create toolbox-identity
    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"
    ```

3.  **Upload the `tools.yaml` file as a secret and set the image variable**:

    ```shell
    gcloud secrets create tools --data-file tools.yaml \
    --replication-policy="user-managed" --locations="us-central1"
    export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
    ```

4.  **Deploy to Cloud Run**:

    ```shell
    gcloud run deploy toolbox \
    --image $IMAGE \
    --service-account toolbox-identity \
    --region us-central1 \
    --set-secrets "/app/tools.yaml=tools:latest" \
    --args="--tools_file=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
    --allow-unauthenticated
    ```

### Deploy the Agent Application

1.  In your `my-agents/looker-agent/agent.py` file, **update the `ToolboxSyncClient` URL to your new Cloud Run service URL**.

2.  **Navigate to the `my-agents` directory and define the following variables**:

    ```shell
    export GOOGLE_CLOUD_PROJECT="YOUR PROJECT ID"
    export GOOGLE_CLOUD_LOCATION="YOUR REGION"
    export AGENT_PATH="looker-agent/"
    export SERVICE_NAME="looker-service"
    export APP_NAME="looker-app"
    export GOOGLE_GENAI_USE_VERTEXAI=True
    ```

4.  **Deploy the agent application to Cloud Run**:

    ```shell
    adk deploy cloud_run \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --service_name=$SERVICE_NAME \
    --app_name=$APP_NAME \
    --with_ui \
    $AGENT_PATH
    ```

Mission Accomplished! 🚀
You have successfully created and deployed your agent. You can now use it anytime from the Cloud Run URL provided by the final deployment command.
