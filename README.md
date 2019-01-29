# LambdaMaths: Team SSA's ICHack19 Project


#### Messenger Chatbot
LambdaMaths is a prototypical messenger chatbot with the lofty aim of having students do their homework on Facebook Messenger. Students appreciate having automated tools that check their work instantly and give them transparent and instant feedback, tools that do this exist. They are also annoying and clunky to use, requiring you to login through their various portals and use their dated UI.

LambdaMaths changes that. Kids have Messenger open almost constantly and work well with doing short bursts of work, both in terms of productivity and accuracy. Students interact with a chatbot, either of their own volition because they want to practice various skills, asking for anything from practice on a certain topic to generating an entire quiz covering the years material for them. More importantly, they can do this as many times as they want: we generate the questions on the fly using various algorithms that take into account the students progress with their past questions, their target and predicted grade and various other factors to ensure they are being sufficiently challenged and learning.

#### Teachers dashboard

Teachers can also set specific homework through the chatbot, via their dashboard, which is not only useful for setting homework, but also for getting a quick glance of everything about their various classrooms, ranging from big-picture average-success rate of their entire class or cohort, to smaller detail like being able to see students troubles with a specific question or their success rate on a given topic. This gives them the opportunity to tackle issues their students are facing early on and improves the transparency of the students progress on both the educator and students side.

#### Trying it out

Come on over to table 6 and give it a try. It's currently in development mode, so you'll need to try it on one of the developers phones/laptops or request to be added as a tester!

#### Technology used

The backend of our project was built with Python, specifically using Flask to interact with Facebook's Messenger API to get, process and reply to messages sent to the chatbot. We used postgresql to keep track of our users details and their progress and difficulties with questions they were trying. This lets us give students a brief summary of their progress in the chatbot itself, but is mainly there to share the data with their teachers, who have a dashboard, built mainly with Javascript and jQuery to display and visualise this data on both a macroscopic and individualistic view. jQuery sends AJAX requests to some of our Flask endpoints to interact with students, namely assigning them homework or answering their comments.

We used git for our version control and our CI/CD pipeline, where pushing to git master immediately triggered some of our tests and deployed the release on Heroku.

#### Privacy

As the teachers communicate through LambdaMaths, they are only able to see which questions they answer, and whether they answered it correctly, along with the comments they provide. 
