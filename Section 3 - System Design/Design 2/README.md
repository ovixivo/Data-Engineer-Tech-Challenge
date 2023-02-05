## Section3: System Design
### Design 2

This section will cover the designing of a system architecture for a company whose main business is in processing image.

draw.io is used in this section to draw the diagram 

 
### Summary of task:

1. Design a system architecture diagram with the following requirements:
   - Web application for users to upload images via API
   - Web application for users to batch upload images via Kafka stream
     - Kafka stream will be managed by in-house engineers
   - Cloud processing of images
   - Business intelligence resource on the cloud for analyst to perform analysis on data
   - High availability with disaster recovery
2. To provide documentation on the architecture.

---

### Proposed design

![alt text](https://github.com/ovixivo/Data-Engineer-Tech-Challenge/blob/main/Section%203%20-%20System%20Design/Design%202/Cloud%20data%20infrastructure%20system%20architecture%20diagram.png "System Architecture")

The architecture is design with hybrid cloud architecture.
There are 2 environments in the setup, firstly on premise, secondly Azure Cloud.

This design allow the company to host lightweight applications and servers locally, while pushing resource heavy tasks to the cloud.

---

### On premise environment

The following servers will be hosted locally:
1. Web Server
2. API Application Server
3. Kafka Cluster
4. Git Server
5. Backup Database Server

By hosting these lightweight server locally, company can save additional cost by reducing the reliance of cloud server.
Furthermore, company will have more control and overview of data coming in and out of the servers.
For example, hosting a local Git repository reduce the risk of source code leak and by using CI/CD pipeline complied source code can be pushed down to predefined servers for faster deployment.

By having users connecting through on premise web server, it is able to prevent direct access to the primary database in the cloud.

#### Web Server

Web server will be used to host 2 web applications.
Firstly, an API web application that allows users to upload images via API.
Secondly, a batch upload web application that allows users to upload large set of images through Kafka stream.
The web server act as the first layer of defence by ensuring only valid user have access to the web page. 
Furthermore, with the use of SSL enabled data send over the web will be secured.

#### API Application Server

The API Application Server will process users' API requests. By setting up locally, latency to process the API is reduced.
In the case of high load, engineers can set up more API applications running on the server and balance the load using load balancer application such as HAProxy.

#### Kafka Cluster

The Kafka Cluster will process batch image upload requests. 
With the cluster managed locally, in the case when network to the cloud is down, batch files will still retain in the server for future processing.
Furthermore, Kafka can be easily scales up by adding more brokers to handle requests without adding more servers.

#### Git Server

The Git Server, such as GitLab, will allow developer to version control their development codes, and with CI/CD pipelines time to deployment of new features can be reduced.
With local Git Server source code leak is also reduced as the company will have more control over who and what is being accessed.

#### Backup Database Server

The Backup Database Server is a cold storage solution to backup data from the cloud.
This allows disaster recovery, in the case where data in the cloud is lost.
Furthermore, the server can act as an archival server to reduce the storage required in the cloud.

### On Azure Cloud environment

The following services will be provision on the cloud:
1. Azure HDInsight
2. Storage blob
3. Kubernetes
4. Image Processing Pod
5. Database Server
6. Azure Analysis Services
7. Azure Databricks

The services and applications running on the cloud is of computation heavy.
By off loading these services to the cloud, company does not have to invest in high-end servers on the premise.
Furthermore, services such as Azure Analysis Services/ Azure Databricks can be start or pause on demand to reduce cost.
With Azure Security, Microsoft also provide a secure environment to process and store data from the users.

#### Azure HDInsight

Azure HDInsight is integrated with Kafka, this will allow the local Kafka cluster to easily connect to the cloud via HDInsight and send the file to a cloud blob storage.
Azure HDInsight also provide easy scaling of Kafka broker through their UI.

#### Storage blob

Azure Storage blob is a temporary cloud storage for storing of images and their metadata.
Data will come from API application and Kafka stream from Azure HDInsight.
The storage will be accessed by image processing application for the processing.
By using Azure Storage lifecycle management policies, engineer can set up rules to remove images and its metadata after 7 days to for compliance and privacy.

#### Kubernetes

With Kubernetes service, engineers can automate deployment, scaling, and management of containerized applications in a centralized location.
The main usage will be used to create and scale Image Processing Pod for the processing of data.
Container image can be pushed to Kubernetes from Git repository hence reducing time to deployment.

#### Image Processing Pod

As image processing is of high computation, it is proposed to use containerized application to enable easy scaling of application.
By setting up Kubernetes Pod, multiple Image Processing containers can be created to server the users need.
Pod can also be automatically scaled based on demand with Kubernetes Horizontal Pod Autoscaler.

#### Database Server

The database server will be used to collect data generated from the image processing.
By using Azure Database Service, data are stored encrypted at rest and in motion.
Data is protected by Azure to ensure only authorized personnel is able to access its content.

#### Azure Analysis Services

Azure Analysis Services provides BI semantic modeling that can be scaled on demand.
This allows users to build data models that can be used for data visualization in Azure Databricks.

#### Azure Databricks

Azure Databricks a collaborative analytics platform that allows analysts to analyze and build machine learning models on the data.
The collaborative environment allow different analysts to work on the same project together with version control and sharing features.
Computational power can also be scaled on demand for better management of cost.

---

### Design Workflow

#### Workflow 1 - API upload
1. A user access a web page that allow uploading of a single image for processing.
2. The image is uploaded using API call to the server
3. The API server push the data onto Azure blob storage
4. Image processing application pick up the new image file for processing
5. The processing result is saved into Azure Database
6. Image processing application return result to user

#### Workflow 2 - Batch upload
1. A user access a web page that allow uploading of a batch of images for processing
2. The image is uploaded and process by a Kafka steam
3. Kafka steam connects to Azure HDInsight to upload the file onto Azure blob storage
4. Image processing application pick up image batch for processing
5. Due to high load, Kubernetes auto-scale image processing pod for faster processing
6. The processing result is saved into Azure Database
7. Image processing application return batch result to user
8. Kubernetes auto-scale image processing pod down as resource is no longer required

#### Workflow 3 - New deployment
1. An engineer has complete a new feature for image processing application
2. An engineer commit the new feature into Git and submitted a merge request
3. A senior engineer review and approve the request
4. Code goes through CI/CD pipeline for testing
5. Upon successful testing, container image is push to Kubernetes for deployment
6. Kubernetes updates pod with the latest container image

#### Workflow 4 - Data analysis
1. An analyst access Azure Analysis Services to build data model of database
2. Using Azure Databricks, the analyst connect to Azure Analysis Services and pull the data model information of the database
3. Using the data model information, analyst create report and dashboard for data analysis
4. To further analyze the data, analyst connect to Azure Databricks to run python scripts that computes in the cloud for faster processing.
5. With the analysis information, analyst can build machine learning models for business use case

---



