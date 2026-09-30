"""Course outline. Chapter selection, ordering and priority/difficulty tags are credited to
AlgoMaster.io (System Design Interviews course roadmap). Content in this repo is original."""
H,M,L='High','Medium','Low'
B,I,A='Beginner','Intermediate','Advanced'
# (folder, section title, kind, items) ; item = (slug, title, priority, difficulty)
# kind 'file' => folder/NN-slug.md ; kind 'dir' => folder/Slug/README.md (slug is folder name)
SECTIONS=[
('01-Introduction','Introduction','file',[
 ('01-what-are-system-design-interviews','What are System Design Interviews?',H,B),
 ('02-types-of-system-design-questions','Types of System Design Questions',H,B),
 ('03-expectations-by-level','Expectations by Level/YoE',H,B),
 ('04-study-plan','Study Plan (bonus)',None,None)]),
('02-Must-Know-Topics','Must-Know Topics','file',[
 ('01-concepts','Concepts',H,B),('02-technologies','Technologies',H,B),
 ('03-tradeoffs','Tradeoffs',H,I),('04-data-structures','Data Structures',M,I)]),
('03-Concept-Deep-Dives','Concept Deep Dives','mixed',[
 ('01-networking','Networking',H,B),('02-caching','Caching',H,I),('03-api-design','API Design',H,I),
 ('04-database-design','Database Design',H,I),('05-Distributed-Systems','Distributed Systems',H,A)]),
('04-Technology-Deep-Dives','Technology Deep Dives','file',[
 ('01-postgresql','PostgreSQL',H,I),('02-mongodb','MongoDB',M,I),('03-redis','Redis',H,I),
 ('04-dynamodb','DynamoDB',H,I),('05-cassandra','Cassandra',H,A),('06-elasticsearch','Elasticsearch',H,I),
 ('07-kafka','Kafka',H,I),('08-rabbitmq','RabbitMQ',M,I),('09-sqs','SQS',M,I),('10-flink','Flink',L,A),
 ('11-s3','S3',H,I),('12-zookeeper','ZooKeeper',M,A)]),
('05-Interview-Patterns','Interview Patterns','file',[
 ('01-scaling-read-traffic','Scaling Read Traffic',H,I),('02-scaling-write-traffic','Scaling Write Traffic',H,I),
 ('03-handling-hot-keys','Handling Hot Keys',H,I),('04-absorbing-traffic-spikes','Absorbing Traffic Spikes',H,I),
 ('05-pushing-realtime-updates','Pushing Real-time Updates',H,I),('06-fanning-out-updates','Fanning Out Updates',H,I),
 ('07-uploading-and-serving-large-files','Uploading and Serving Large Files',M,I),
 ('08-streaming-video-and-audio','Streaming Video and Audio',H,A),
 ('09-surviving-component-failures','Surviving Component Failures',H,I),
 ('10-preventing-duplicate-processing','Preventing Duplicate Processing',H,I),
 ('11-running-across-multiple-regions','Running Across Multiple Regions',M,A),
 ('12-coordinating-transactions-across-services','Coordinating Transactions Across Services',M,A),
 ('13-keeping-data-in-sync','Keeping Data in Sync',H,I),('14-preventing-double-booking','Preventing Double Booking',H,I),
 ('15-handling-long-running-tasks','Handling Long-Running Tasks',H,I),
 ('16-scheduling-delayed-and-recurring-jobs','Scheduling Delayed and Recurring Jobs',M,I),
 ('17-search-and-typeahead','Search and Typeahead',H,I),('18-finding-and-tracking-locations','Finding and Tracking Locations',H,I),
 ('19-generating-unique-ids','Generating Unique IDs',M,I),('20-counting-at-scale','Counting at Scale',M,A)]),
('06-Interview-Tips','Interview Tips','file',[
 ('01-answering-framework','Answering Framework',H,B),('02-estimation-cheatsheet','Estimation Cheatsheet',H,B),
 ('03-diagramming-tips','Diagramming Tips',H,B),('04-choosing-the-right-database','Choosing the Right Database',H,I)]),
('07-Basic-Questions','Basic Questions','dir',[
 ('URL-Shortener','Design URL Shortener',H,B),('Pastebin','Design Pastebin',M,B)]),
('08-Real-Time-Communication','Real-Time Communication','dir',[
 ('WhatsApp','Design WhatsApp',H,I),('Slack','Design Slack',M,I),('Live-Comments','Design Live Comments',M,I),
 ('Google-Docs','Design Google Docs',H,A),('Zoom','Design Zoom',M,A)]),
('09-Social-Media-Systems','Social Media Systems','dir',[
 ('Instagram','Design Instagram',H,I),('FB-News-Feed','Design FB News Feed',H,I),('TikTok','Design TikTok',M,I),
 ('Reddit','Design Reddit',M,I),('Tinder','Design Tinder',M,I)]),
('10-Media-Streaming-and-Delivery','Media Streaming & Delivery','dir',[
 ('Spotify','Design Spotify',M,I),('YouTube','Design YouTube',H,I),('Netflix','Design Netflix',H,I),
 ('Google-Drive','Design Google Drive',H,I),('Gmail','Design Gmail',L,A),('Twitch','Design Twitch',M,A)]),
('11-Location-Based-Services','Location-Based Services','dir',[
 ('Airbnb','Design Airbnb',M,I),('Food-Delivery-Service','Design Food Delivery Service',M,I),
 ('Uber','Design Uber',H,A),('Google-Maps','Design Google Maps',M,A),
 ('Nearby-Places-Bonus','Design Nearby Places / Yelp (bonus)',None,None)]),
('12-Search-and-Aggregation-Systems','Search & Aggregation Systems','dir',[
 ('Search-Autocomplete','Design Search Autocomplete System',H,B),('News-Aggregator','Design News Aggregator',L,I),
 ('Web-Crawler','Design Web Crawler',H,I),('Google-Search','Design Google Search',M,A),
 ('Ad-Click-Aggregator','Design Ad Click Aggregator',M,A)]),
('13-E-commerce-and-Marketplace','E-commerce & Marketplace','dir',[
 ('Amazon','Design Amazon',M,I),('Shopify','Design Shopify',L,I),('Flash-Sale','Design Flash Sale',M,A),
 ('Online-Auction-System','Design Online Auction System',L,A),('Movie-Booking','Design Movie Booking System',M,A)]),
('14-Payment-and-Financial-Systems','Payment & Financial Systems','dir',[
 ('Payment-System','Design Payment System',H,I),('Digital-Wallet','Design Digital Wallet',M,A),
 ('Stock-Exchange','Design Stock Exchange',L,A)]),
('15-Distributed-Infrastructure','Distributed Infrastructure','dir',[
 ('Load-Balancer','Design Load Balancer',H,I),('API-Gateway','Design API Gateway',H,I),
 ('Rate-Limiter','Design Rate Limiter',H,I),('Key-Value-Store','Design Key-Value Store',H,A),
 ('Distributed-Cache','Design Distributed Cache',H,A),('CDN','Design CDN',M,A),
 ('Object-Storage-S3','Design Object Storage like S3',M,A),('Messaging-Queue','Design Messaging Queue',M,A),
 ('Time-Series-Database','Design Time Series Database',L,A),('Locking-Service','Design Locking Service',L,A)]),
('16-Counting-and-Ranking-Systems','Counting & Ranking Systems','dir',[
 ('Likes-Counting-System','Design Likes Counting System',M,I),('Real-Time-Leaderboard','Design Real Time Leaderboard',M,I),
 ('Top-K','Design Top K',M,A)]),
('17-Asynchronous-Systems','Asynchronous Systems','dir',[
 ('Notification-Service','Design Notification Service',H,I),('Job-Scheduler','Design Job Scheduler',M,I),
 ('CI-CD-Pipeline','Design CI/CD Pipeline',L,I),('Monitoring-and-Alerting','Design Monitoring and Alerting System',M,I)]),
('18-Specialized-Systems','Specialized Systems','dir',[
 ('LeetCode','Design LeetCode',M,I),('Calendar-System','Design Calendar System',L,A),
 ('Online-Chess','Design Online Chess',L,A)]),
]
ROADMAP_URL='https://algomaster.io/learn/system-design-interviews/course-roadmap'
def item_path(sec,item):
    folder,_,kind,_=sec; slug=item[0]
    if kind=='dir': return f'{folder}/{slug}/README.md'
    if kind=='mixed' and slug=='05-Distributed-Systems': return f'{folder}/{slug}/README.md'
    return f'{folder}/{slug}.md'
