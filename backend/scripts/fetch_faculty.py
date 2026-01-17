import os
import requests
import time
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models import Faculty, Paper

load_dotenv()

S2_API = "https://api.semanticscholar.org/graph/v1"
S2_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

HEADERS = {"x-api-key": S2_API_KEY} if S2_API_KEY else {}

# =============================================================================
# FACULTY BY SCHOOL - Organized by Department/Field
# Categories: CS, Statistics, Data Science, Applied Math
# US Universities Only
# =============================================================================

# --- COMPUTER SCIENCE (AI/ML, Systems, Theory, Security, HCI) ---
CS_FACULTY = {
    "MIT CS": [
        "Regina Barzilay", "Hal Abelson", "Kaiming He", "Tommi Jaakkola", "Leslie Kaelbling",
        "Aleksander Madry", "Wojciech Matusik", "Ankur Moitra", "David Sontag", "Justin Solomon",
        "Vivienne Sze", "Erik Demaine", "Constantinos Daskalakis", "Piotr Indyk", "Silvio Micali",
        "Ronald Rivest", "Shafi Goldwasser", "Hari Balakrishnan", "Barbara Liskov", "Samuel Madden"
    ],
    "Stanford CS": [
        "Fei-Fei Li", "Christopher Manning", "Andrew Ng", "Dan Boneh", "Moses Charikar",
        "Chelsea Finn", "Stefano Ermon", "Leonidas Guibas", "Carlos Guestrin", "Emma Brunskill",
        "Percy Liang", "Jure Leskovec", "Christopher Ré", "Diyi Yang", "John Hennessy",
        "Michael Bernstein", "Ron Fedkiw", "Jeannette Wing", "James Landay", "Dan Jurafsky"
    ],
    "CMU CS": [
        "Tom Mitchell", "Ruslan Salakhutdinov", "Geoff Gordon", "Manuela Veloso",
        "Christos Faloutsos", "Guy Blelloch", "Martial Hebert",
        "Eric Xing", "Roni Rosenfeld", "Katia Sycara", "Tuomas Sandholm",
        "Graham Neubig", "Fernando Diaz", "Mona Diab", "Deepak Pathak", "Deva Ramanan"
    ],
    "UC Berkeley CS": [
        "Michael I. Jordan", "Stuart Russell", "Pieter Abbeel", "Dawn Song", "Trevor Darrell",
        "Dan Klein", "Joseph Gonzalez", "Ion Stoica", "Ken Goldberg", "John Canny",
        "Anca Dragan", "Alexei Efros", "Jitendra Malik", "Michael Mahoney", "Peter Bartlett",
        "David Wagner", "Umesh Vazirani", "Alistair Sinclair", "Sanjit Seshia", "Jennifer Chayes"
    ],
    "UW CS": [
        "Pedro Domingos", "Emily Fox", "Ali Farhadi", "Luke Zettlemoyer", "Noah Smith",
        "Yejin Choi", "Dan Weld", "Oren Etzioni", "Jeff Heer", "Magdalena Balazinska",
        "Shyam Gollakota", "Rajesh Rao", "Dieter Fox", "Maya Cakmak", "Hannaneh Hajishirzi",
        "Linda Shapiro", "Ranjay Krishna", "Tim Althoff"
    ],
    "Cornell CS": [
        "Jon Kleinberg", "Thorsten Joachims", "Claire Cardie", "Bart Selman", "Kilian Weinberger",
        "Kavita Bala", "Serge Belongie", "Karthik Sridharan", "Christopher De Sa", "Adrian Sampson",
        "Lorenzo Alvisi", "Rachit Agarwal", "Yoav Artzi", "David Bindel", "Ken Birman",
        "Alexander Rush", "Noah Snavely", "Steve Marschner"
    ],
    "Princeton CS": [
        "Sanjeev Arora", "Kai Li", "Jennifer Rexford", "Olga Russakovsky", "Karthik Narasimhan",
        "Danqi Chen", "Mengdi Wang", "Jason Lee", "Chi Jin", "Elad Hazan",
        "Robert Tarjan", "Bernard Chazelle", "Aarti Gupta", "David Walker", "Andrew Appel",
        "Brian Kernighan", "Margaret Martonosi", "Prateek Mittal", "Arvind Narayanan", "Matt Weinberg"
    ],
    "UT Austin CS": [
        "Scott Aaronson", "Peter Stone", "Kristen Grauman", "Raymond Mooney", "Inderjit Dhillon",
        "Swarat Chaudhuri", "Philipp Krähenbühl", "Greg Plaxton", "Adam Klivans", "Işıl Dillig",
        "Qiang Liu", "Dana Moshkovitz", "Joydeep Biswas", "Risto Miikkulainen",
        "David Harwath", "Roberto Martin-Martin", "Qixing Huang", "Warren Hunt", "Vijaya Ramachandran"
    ],
    "UIUC CS": [
        "Jiawei Han", "Chengxiang Zhai", "Heng Ji", "David Forsyth", "Svetlana Lazebnik",
        "Julia Hockenmaier", "Derek Hoiem", "Marc Snir", "Vikram Adve",
        "Sarita Adve", "Josep Torrellas", "Tarek Abdelzaher", "Brighten Godfrey", "Matthew Caesar",
        "Lingming Zhang", "Tianyin Xu", "Nan Jiang", "Bo Li", "Sanmi Koyejo"
    ],
    "Georgia Tech CS": [
        "Charles Isbell", "Mark Riedl", "Devi Parikh", "Dhruv Batra", "Zsolt Kira",
        "Joy Arulraj", "Ada Gavrilovska", "Santosh Pande", "Taesoo Kim", "Wenke Lee",
        "Alexandra Boldyreva", "Mostafa Ammar", "Constantine Dovrolis",
        "Irfan Essa", "Frank Dellaert", "Ashok Goel", "Polo Chau"
    ],
    "UCLA CS": [
        "Judea Pearl", "Guy Van den Broeck", "Cho-Jui Hsieh", "Quanquan Gu", "Kai-Wei Chang",
        "Aditya Grover", "Bolei Zhou", "Achuta Kadambi", "Songwu Lu", "Todd Millstein",
        "Miryung Kim", "George Varghese", "Mani Srivastava", "Rafail Ostrovsky", "Amit Sahai",
        "Leonard Kleinrock", "Majid Sarrafzadeh", "Yizhou Sun", "Wei Wang"
    ],
    "UMich CS": [
        "H. V. Jagadish", "Michael Wellman", "Rada Mihalcea", "Dragomir Radev", "Jenna Wiens",
        "Joyce Chai", "Danai Koutra", "Satinder Singh", "Honglak Lee", "David Fouhey",
        "Eytan Adar", "Wei Lu", "Qiaozhu Mei",
        "Laura Balzano", "Grant Schoenebeck", "Karem Sakallah"
    ],
    "Columbia CS": [
        "Julia Hirschberg", "Kathy McKeown", "Zhou Yu", "Smaranda Muresan", "Carl Vondrick",
        "Daniel Hsu", "Tim Roughgarden", "Christos Papadimitriou", "Tal Malkin", "Rocco Servedio",
        "David Blei", "John Paisley", "Nakul Verma", "Allison Bishop", "Gail Kaiser",
        "Jason Nieh", "Roxana Geambasu", "Simha Sethumadhavan", "Augustin Chaintreau", "Eugene Wu"
    ],
    "NYU CS": [
        "Yann LeCun", "Rob Fergus", "Kyunghyun Cho", "Sam Bowman", "He He",
        "Lerrel Pinto", "Rajesh Ranganath", "Joan Bruna", "Claudio Silva", "Torsten Suel",
        "Dennis Shasha", "Ernest Davis", "Subhash Khot", "Richard Zemel", "Julia Stoyanovich",
        "Damon McCoy", "Rachel Greenstadt", "Michael Overton", "Mehryar Mohri", "Yevgeniy Dodis"
    ],
    "Harvard CS": [
        "Leslie Valiant", "Michael Mitzenmacher", "Sham Kakade", "Cynthia Dwork", "Salil Vadhan",
        "David Parkes", "Yiling Chen", "Barbara Grosz", "Stuart Shieber", "Finale Doshi-Velez",
        "Hanspeter Pfister", "Stratos Idreos", "Eddie Kohler", "James Mickens", "David Malan",
        "Milind Tambe", "Krzysztof Gajos", "Hima Lakkaraju", "Stephen Chong", "Todd Zickler"
    ],
    "Yale CS": [
        "Joan Feigenbaum", "Steven Zucker", "Dana Angluin", "Zhong Shao",
        "Julie Dorsey", "Holly Rushmeier", "Brian Scassellati", "David Gelernter", "Ruzica Piskac",
        "Yang Cai", "James Aspnes", "Daniel Abadi",
        "Mahesh Balakrishnan", "Lin Zhong", "Abhishek Bhattacharjee", "Rajit Manohar", "Jakub Szefer"
    ],
    "Brown CS": [
        "Michael Littman", "Stefanie Tellex", "George Konidaris", "Ellie Pavlick", "Eugene Charniak",
        "Carsten Eickhoff", "Jeff Huang", "Anna Lysyanskaya", "Roberto Tamassia", "Eli Upfal",
        "Shriram Krishnamurthi", "Tim Nelson", "Malte Schwarzkopf", "Srinath Sridhar", "Chen Sun",
        "Ritambhara Singh", "Daniel Ritchie", "James Tompkin", "Philip Klein", "Maurice Herlihy"
    ],
    "USC CS": [
        "Aram Galstyan", "Yan Liu", "Muhao Chen", "Xiang Ren", "Swabha Swayamdipta",
        "Phebe Vayanos", "Sven Koenig", "Gaurav Sukhatme", "Stefan Schaal",
        "Viktor Prasanna", "Jyotirmoy Deshmukh",
        "Barath Raghavan", "Christos Papadopoulos", "Bhaskar Krishnamachari", "Cyrus Shahabi"
    ],
    "UCSD CS": [
        "Julian McAuley", "Jingbo Shang", "Taylor Berg-Kirkpatrick", "Ndapa Nakashole", "Yoav Freund",
        "Sanjoy Dasgupta", "Kamalika Chaudhuri", "Mihir Bellare", "Daniele Micciancio", "Stefan Savage",
        "Hovav Shacham", "Deian Stefan", "Ravi Ramamoorthi", "Hao Su", "Henrik Christensen",
        "Sicun Gao", "Ryan Kastner", "Steven Swanson", "George Porter", "Tajana Rosing"
    ],
    "UMass Amherst CS": [
        "Andrew McCallum", "Mohit Iyyer", "Brendan O'Connor", "Chuang Gan", "Madalina Fiterau",
        "Daniel Sheldon", "Erik Learned-Miller", "Subhransu Maji", "Ben Marlin", "Hava Siegelmann",
        "Ramesh Sitaraman", "Prashant Shenoy", "Don Towsley", "Deepak Ganesan", "Emery Berger",
        "Yair Zick", "Justin Domke", "Bruno Castro da Silva", "Philip Thomas", "David Jensen"
    ],
    "UMaryland CS": [
        "Tom Goldstein", "Furong Huang", "Jordan Boyd-Graber", "Marine Carpuat", "Hal Daumé III",
        "Dinesh Manocha", "Abhinav Shrivastava", "Larry Davis", "David Jacobs", "John Aloimonos",
        "Amol Deshpande", "Hanan Samet", "William Gasarch", "Mohammad Hajiaghayi", "Aravind Srinivasan",
        "Dave Levin", "Bobby Bhattacharjee", "Jeffrey Hollingsworth", "Michelle Mazurek", "Nirupam Roy"
    ],
    "UWisconsin CS": [
        "Jerry Zhu", "Sharon Li", "Yingyu Liang", "Frederic Sala", "Yong Jae Lee",
        "Mohit Gupta", "Bilge Mutlu", "Michael Gleicher", "Charles Dyer", "Remzi Arpaci-Dusseau",
        "Andrea Arpaci-Dusseau", "Somesh Jha", "Thomas Ristenpart", "Aws Albarghouthi", "Paris Koutris",
        "Shivaram Venkataraman", "Jin-Yi Cai", "Dieter van Melkebeek", "Stephen Wright", "Michael Ferris"
    ],
    "UPenn CS": [
        "Chris Callison-Burch", "Dan Roth", "Lyle Ungar", "Mark Yatskar", "Daphne Ippolito",
        "Mayur Naik", "Rajeev Alur", "Benjamin Pierce", "Steve Zdancewic", "Aaron Roth",
        "Michael Kearns", "Sampath Kannan", "Sanjeev Khanna", "Insup Lee", "Zachary Ives",
        "Susan Davidson", "Boon Thau Loo", "Vincent Liu", "Linh Thi Xuan Phan", "George Pappas"
    ],
    "Duke CS": [
        "Cynthia Rudin", "Brandon Fain", "Kamesh Munagala", "Rong Ge", "Debmalya Panigrahi",
        "Alexander Hartemink", "Bruce Donald", "Pankaj Agarwal", "Jeff Chase", "Jun Yang",
        "Michael Reiter", "Kartik Nayak", "Ashwin Machanavajjhala", "Jian Pei", "Bhuwan Dhingra",
        "Carlo Tomasi", "Ronald Parr", "Owen Astrachan", "Susan Rodger"
    ],
    "Northwestern CS": [
        "Kristian Hammond", "Doug Downey", "Samir Khuller", "Konstantin Makarychev", "Aleksandar Kuzmanovic",
        "Yan Chen", "Fabián Bustamante", "Peter Dinda", "Robert Dick", "Josiah Hester",
        "Xinyu Zhang", "Goce Trajcevski", "Aaron Elmore", "Jennie Rogers",
        "Christos Dimoulas", "Xiao Wang", "Alok Choudhary"
    ],
    "Purdue CS": [
        "Dan Goldwasser", "Julia Rayz", "Ming Yin", "David Gleich", "Ananth Grama",
        "Xiangyu Zhang", "Dongyan Xu", "Saurabh Bagchi", "Suresh Jagannathan", "Tiark Rompf",
        "Benjamin Delaware", "Roopsha Samanta", "Aniket Kate", "Christina Garman", "Hemanta Maji",
        "Jeremiah Blocki", "Elisa Bertino", "Samuel Midkiff", "Milind Kulkarni"
    ],
    "Ohio State CS": [
        "Yu Su", "Wei Xu", "Huan Sun", "Alan Ritter", "Srinivasan Parthasarathy",
        "Arnab Nandi", "Rajiv Ramnath", "Michael Bond", "Zhiqiang Lin", "Anish Arora",
        "Ness Shroff", "DK Panda", "Feng Qin",
        "Eric Fosler-Lussier", "Mikhail Belkin", "Christopher Stewart"
    ],
    "Virginia Tech CS": [
        "Ismini Lourentzou", "Chris North", "Kurt Luther", "Ryan McMahan",
        "Christine Julien", "Ali Butt", "T. M. Murali", "Danfeng Zhang", "Wenjing Lou",
        "Bo Ji", "Yang Cao", "Jia-Bin Huang",
        "Chang-Tien Lu", "Naren Ramakrishnan", "Anuj Karpatne", "Bert Huang"
    ],
    "Caltech CS": [
        "Yisong Yue", "Katie Bouman", "Adam Wierman", "Anima Anandkumar", "Pietro Perona",
        "Thomas Vidick", "Joel Tropp", "Venkat Chandrasekaran", "Chris Umans", "Leonard Schulman",
        "Yaser Abu-Mostafa", "Babak Hassibi", "Michelle Effros", "Tracey Ho"
    ]
}

# --- STATISTICS ---
STATS_FACULTY = {
    "Stanford Stats": [
        "Emmanuel Candes", "Persi Diaconis", "David Donoho", "Bradley Efron",
        "Trevor Hastie", "Susan Holmes", "Iain Johnstone", "Andrea Montanari",
        "Art Owen", "Chiara Sabatti", "Robert Tibshirani", "Jonathan Taylor"
    ],
    "Berkeley Stats": [
        "Peter Bickel", "Bin Yu", "Michael Jordan", "Jennifer Chayes",
        "Peng Ding", "Avi Feller", "Will Fithian", "Haiyan Huang",
        "Song Mei", "Fernando Perez", "Philip Stark", "Mark van der Laan"
    ],
    "UChicago Stats": [
        "Rina Barber", "Dan Nicolae", "Mary Sara McPeek", "Per Mykland",
        "Matthew Stephens", "Rebecca Willett", "Wei Biao Wu", "Yali Amit",
        "Chao Gao", "Gregory Lawler", "Veronika Rockova", "Nati Srebro"
    ],
    "Columbia Stats": [
        "David Blei", "Andrew Gelman", "Tian Zheng", "Richard Davis",
        "John Cunningham", "Genevera Allen", "David Madigan", "Zhiliang Ying",
        "Philip Protter"
    ],
    "Harvard Stats": [
        "Xiao-Li Meng", "Donald Rubin", "Jun Liu", "Susan Murphy",
        "Kosuke Imai", "Joseph Blitzstein", "Tracy Ke", "Lucas Janson",
        "Natesh Pillai", "Pragya Sur", "Xihong Lin", "Morgane Austern"
    ],
    "UW Stats": [
        "Daniela Witten", "Thomas Fleming", "Adrian Dobra", "Elena Erosheva",
        "Fang Han", "Zaid Harchaoui", "Thomas Richardson", "Abel Rodriguez",
        "Ali Shojaie", "Jon Wakefield", "Yen-Chi Chen", "Tyler McCormick"
    ],
    "CMU Stats": [
        "Larry Wasserman", "Kathryn Roeder", "Rob Kass", "Chad Schafer",
        "Jiashun Jin", "Rebecca Nugent", "Cosma Shalizi", "Ann Lee",
        "Siva Balakrishnan", "Arun Kuchibhotla", "Aaditya Ramdas", "Edward Kennedy"
    ],
    "Duke Stats": [
        "David Dunson", "Merlise Clyde", "Jerome Reiter", "Amy Herring",
        "Peter Hoff", "Mike West", "Alan Gelfand", "Fan Li",
        "Alexander Volfovsky", "Surya Tokdar", "Eric Laber"
    ],
    "UMich Stats": [
        "Elizaveta Levina", "Ji Zhu", "Kerby Shedden", "Xuming He",
        "Ambuj Tewari", "Yang Chen", "Long Nguyen", "Stilian Stoev",
        "Alfred Hero", "Gongjun Xu", "Tailen Hsing"
    ],
    "Cornell Stats": [
        "David Matteson", "Sumanta Basu", "James Booth", "Florentina Bunea",
        "Giles Hooker", "Martin Wells", "Marten Wegkamp", "Nathan Kallus",
        "Michael Nussbaum", "Jacob Bien"
    ],
    "Penn Wharton Stats": [
        "Tony Cai", "Larry Brown", "Andreas Buja", "Ed George",
        "Dylan Small", "Abraham Wyner", "Nancy Zhang", "Linda Zhao",
        "Weijie Su", "Shane Jensen", "Bhaswar Bhattacharya", "Edgar Dobriban"
    ],
    "Yale Stats": [
        "Andrew Barron", "Joseph Chang", "John Hartigan",
        "Zhou Fan", "Yihong Wu", "Harrison Zhou", "John Lafferty",
        "Roy Lederman", "Dan Spielman", "Sekhar Tatikonda", "Zhuoran Yang"
    ],
    "UNC Stats": [
        "J. S. Marron", "Yufeng Liu", "Andrew Nobel", "Jan Hannig",
        "Shankar Bhamidi", "Richard Smith", "Haipeng Shen", "Kai Zhang",
        "Chuanshu Ji", "Amarjit Budhiraja", "Vladas Pipiras", "Sayan Banerjee"
    ],
    "Wisconsin Stats": [
        "Grace Wahba", "Michael Newton", "Jun Shao", "Sunduz Keles",
        "Yazhen Wang", "Garvesh Raskutti", "Karl Rohe", "Keith Levin",
        "Sameer Deshpande", "Wei-Yin Loh", "Chunming Zhang", "Hyunseung Kang"
    ],
    "Minnesota Stats": [
        "Charles Geyer", "Christopher Nachtsheim", "Gary Oehlert", "Hui Zou",
        "Galin Jones", "Adam Rothman", "Xiaotong Shen", "Lan Wang",
        "Snigdhansu Chatterjee", "Tiefeng Jiang", "Aaron Molstad", "Yuhong Yang"
    ],
    "Purdue Stats": [
        "Mary Ellen Bock", "Dennis Lin", "Guang Cheng",
        "Faming Liang", "Chuanhai Liu", "Xiao Wang", "Anindya Bhadra",
        "Jun Xie", "Vinayak Rao", "Hao Zhang", "Bruce Craig"
    ],
    "Iowa State Stats": [
        "Alicia Carriquiry", "Stephen Vardeman", "Dan Nettleton", "Ranjan Maitra",
        "Jae-Kwang Kim", "Kris De Brabanter", "Jarad Niemi", "Peng Liu",
        "Ulrike Genschel", "Petruta Caragea", "Mark Kaiser", "Vivekananda Roy"
    ],
    "NC State Stats": [
        "Marie Davidian", "Len Stefanski", "Dennis Boos", "Montserrat Fuentes",
        "Brian Reich", "Subhashis Ghoshal", "Eric Laber", "Wenbin Lu",
        "Sujit Ghosh", "Ana-Maria Staicu", "Jung-Ying Tzeng", "Ryan Martin"
    ],
    "UCLA Stats": [
        "Mark Handcock", "Jan de Leeuw", "Rick Schoenberg", "Sudipto Banerjee",
        "Ying Nian Wu", "Nicolas Christou", "Frederic Paik Schoenberg",
        "Chad Hazlett", "Qing Zhou", "Marc Suchard", "Hua Zhou"
    ],
    "Johns Hopkins Biostat": [
        "Scott Zeger", "Karen Bandeen-Roche", "Brian Caffo", "Marie Diener-West",
        "Ciprian Crainiceanu", "Jeff Leek", "Rafael Irizarry", "Martin Lindquist",
        "Elizabeth Stuart", "John McGready", "Roger Peng", "Abhirup Datta"
    ],
    "Rice Stats": [
        "Marek Kimmel", "Dennis Cox", "Marina Vannucci", "Genevera Allen",
        "Rudy Guerra", "Katherine Ensor", "Michelle Lacey", "David Scott",
        "James Thompson", "Michele Guindani", "Philip Ernst"
    ],
    "Texas A&M Stats": [
        "Bani Mallick", "Mohsen Pourahmadi",
        "Suojin Wang", "Xianyang Zhang", "Matthias Katzfuss", "Yang Ni",
        "Rajarshi Guhaniyogi", "Huiyan Sang", "Scott Crawford", "Alan Dabney"
    ]
}

# --- DATA SCIENCE ---
DS_FACULTY = {
    "NYU Data Science": [
        "Yann LeCun", "Kyunghyun Cho", "Joan Bruna", "Samuel Bowman",
        "Andrew Gordon Wilson", "Julia Kempe", "Rajesh Ranganath", "He He",
        "Claudio Silva", "Julia Stoyanovich"
    ],
    "Berkeley Data Science": [
        "Michael Jordan", "Bin Yu", "Jennifer Chayes", "Fernando Perez",
        "Ani Adhikari", "John DeNero", "Joshua Hug", "David Culler",
        "Sandrine Dudoit"
    ],
    "MIT IDSS": [
        "Munther Dahleh", "Devavrat Shah", "Caroline Uhler", "Tamara Broderick",
        "Ankur Moitra", "Guy Bresler", "David Gamarnik", "Daron Acemoglu",
        "Sinan Aral", "Philippe Rigollet"
    ],
    "Columbia Data Science": [
        "David Blei", "Kathleen McKeown", "Elias Bareinboim", "Ryan Abernathey",
        "Shipra Agrawal", "Alexandr Andoni", "Eric Balkanski", "Dana Pe'er",
        "Jose Blanchet", "Vineet Goyal"
    ],
    "Harvard Data Science": [
        "Francesca Dominici", "Stratos Idreos", "Xiao-Li Meng", "Gary King",
        "Melissa Dell", "Alyssa Goodman", "David Parkes", "S.C. Samuel Kou",
        "Sharon-Lise Normand", "Hanspeter Pfister"
    ],
    "Stanford Data Science": [
        "Susan Athey", "Percy Liang", "Jure Leskovec", "Emma Brunskill",
        "James Landay", "Russ Altman", "Curtis Langlotz", "Ludwig Schmidt",
        "Diyi Yang", "Johan Ugander"
    ],
    "UMich MIDAS": [
        "Jenna Wiens", "Rada Mihalcea", "Kayvan Najarian", "Ceren Budak",
        "Eric Gilbert", "Sarita Schoenebeck", "H.V. Jagadish", "Michael Wellman",
        "Alfred Hero"
    ],
    "USC ISI": [
        "Craig Knoblock", "Yolanda Gil", "Yue Wang", "Yan Liu",
        "Aram Galstyan", "Kristina Lerman", "Fred Morstatter", "Emilio Ferrara"
    ],
    "Northwestern Data Science": [
        "Dashun Wang", "Brian Uzzi", "Tom Miller", "Ágnes Horvát",
        "Noshir Contractor", "Diego Klabjan", "Elizabeth Tipton"
    ],
    "CMU Heinz": [
        "Rayid Ghani", "Leman Akoglu", "Alessandro Acquisti", "Eli Ben-Michael",
        "Jonathan Caulkins", "Anupam Datta", "Kathleen Carley", "Rema Padman"
    ],
    "UVA Data Science": [
        "Philip Bourne", "Brian Wright", "Stephen Baek",
        "Peter Beling", "Daniel Graham", "Rafael Alvarado", "Stephen Turner"
    ]
}

# --- APPLIED MATH / OPTIMIZATION / OPERATIONS RESEARCH ---
MATH_FACULTY = {
    "MIT Applied Math": [
        "Michel Goemans", "Pablo Parrilo", "Philippe Rigollet", "Ankur Moitra",
        "Jonathan Kelner", "Alan Edelman", "Laurent Demanet", "Martin Wainwright"
    ],
    "Stanford ICME": [
        "Stephen Boyd", "Emmanuel Candes", "Peter Glynn", "Jose Blanchet",
        "Lexing Ying", "Eric Darve", "Margot Gerritsen", "Robert Tibshirani"
    ],
    "Caltech CMS": [
        "Venkat Chandrasekaran", "Joel Tropp", "Adam Wierman", "Houman Owhadi",
        "Thomas Hou", "Andrew Stuart", "Oscar Bruno", "Yaser Abu-Mostafa"
    ],
    "Berkeley IEOR": [
        "Alper Atamturk", "Anil Aswani", "Dorit Hochbaum", "Paul Grigas",
        "Javad Lavaei", "Xin Guo", "Ying Cui", "Zeyu Zheng"
    ],
    "NYU Courant": [
        "Leslie Greengard", "Michael Overton", "Jonathan Goodman", "Aleksandar Donev",
        "Georg Stadler", "Eric Vanden-Eijnden", "Marsha Berger", "Denis Zorin"
    ],
    "UChicago CAM": [
        "Lek-Heng Lim", "Guillaume Bal", "Rebecca Willett", "Mihai Anitescu",
        "Yuehaw Khoo", "Risi Kondor", "Cong Ma", "Nathan Srebro"
    ],
    "Cornell ORIE": [
        "David Shmoys", "Peter Frazier", "Shane Henderson", "Huseyin Topaloglu",
        "Jim Dai", "Adrian Lewis", "Siddhartha Banerjee", "Jamol Pender"
    ],
    "Princeton ORFE": [
        "Amir Ali Ahmadi", "Jianqing Fan", "Ronnie Sircar", "Mete Soner",
        "Bartolomeo Stellato", "Jason Klusowski", "Ludovic Tangpi", "Boris Hanin"
    ],
    "Columbia IEOR": [
        "Garud Iyengar", "Jay Sethuraman", "Cliff Stein", "Vineet Goyal",
        "Daniel Bienstock", "Assaf Zeevi", "Agostino Capponi", "Adam Elmachtoub"
    ],
    "Georgia Tech ISyE": [
        "Arkadi Nemirovski", "Alexander Shapiro", "Santanu Dey", "Guanghui Lan",
        "Mohit Singh", "Andy Sun", "Alejandro Toriello", "Katya Scheinberg"
    ],
    "UT Austin ORIE": [
        "Constantine Caramanis", "Grani Hanasusanto", "Evdokia Nikolova", "Steve Boyles",
        "John Hasenbein", "Ben Leibowicz", "Ross Baldick", "Erhan Kutanoglu"
    ],
    "Northwestern IEMS": [
        "Jorge Nocedal", "Sanjay Mehrotra", "Simge Küçükyavuz", "David Morton",
        "Diego Klabjan", "Zhaoran Wang", "Karen Smilowitz", "Seyed Iravani"
    ],
    "UMich IOE": [
        "Jon Lee", "Siqian Shen", "Marina Epelman", "Ruiwei Jiang",
        "Cong Shi", "Mark Daskin", "Amy Cohn", "Julie Ivy"
    ],
    "Wisconsin Math": [
        "Alberto Del Pia", "Stephen Wright", "Qin Li", "Christopher Rycroft",
        "Jean-Luc Thiffeault", "Michael Ferris", "Nan Chen", "Hanbaek Lyu"
    ],
    "Brown Applied Math": [
        "George Karniadakis", "Chi-Wang Shu", "Paul Dupuis", "Jerome Darbon",
        "Kavita Ramanan", "Johnny Guzmán", "Brendan Keith", "Hui Wang"
    ],
    "UCLA Applied Math": [
        "Stanley Osher", "Andrea Bertozzi", "Deanna Needell", "Ernest Ryu",
        "Guido Montúfar", "Mason Porter", "Chenfanfu Jiang"
    ],
    "UIUC ISE": [
        "Jugal Garg", "Lavanya Marla", "Carolyn Beck",
        "Alexander Stolyar", "Karthekeyan Chandrasekaran", "Richard Sowers"
    ],
    "Purdue IE": [
        "Gesualdo Scutari", "Nan Kong", "Harsha Honnappa", "Zhe Zhang",
        "Vaneet Aggarwal", "Susan Hunter", "Andrew Liu", "Mario Ventresca"
    ],
    "CMU Tepper": [
        "R. Ravi", "Fatma Kılınç-Karzan", "Javier Peña", "Willem-Jan Van Hoeve",
        "Michael Trick", "Karan Singh", "Andrew Li"
    ]
}

# Combine all faculty into one dictionary for the fetch script
FACULTY_BY_SCHOOL = {}
FACULTY_BY_SCHOOL.update(CS_FACULTY)
FACULTY_BY_SCHOOL.update(STATS_FACULTY)
FACULTY_BY_SCHOOL.update(DS_FACULTY)
FACULTY_BY_SCHOOL.update(MATH_FACULTY)


def search_author(name: str) -> dict | None:
    url = f"{S2_API}/author/search"
    params = {"query": name, "limit": 1}
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("data"):
            return data["data"][0]
    except Exception as e:
        print(f"  Error: {e}")
    return None


def get_author_details(author_id: str) -> dict | None:
    url = f"{S2_API}/author/{author_id}"
    params = {
        "fields": "name,affiliations,homepage,hIndex,citationCount,paperCount,papers.title,papers.year,papers.abstract,papers.venue,papers.citationCount"
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Error: {e}")
    return None


def save_faculty(db: Session, author: dict, school: str) -> Faculty | None:
    existing = db.query(Faculty).filter(
        Faculty.semantic_scholar_id == author["authorId"]
    ).first()

    if existing:
        print(f"  Already exists, skipping")
        return existing

    faculty = Faculty(
        semantic_scholar_id=author["authorId"],
        name=author["name"],
        affiliation=school,
        homepage=author.get("homepage"),
        h_index=author.get("hIndex"),
        citation_count=author.get("citationCount"),
        paper_count=author.get("paperCount"),
    )
    db.add(faculty)
    db.flush()

    papers = author.get("papers", [])
    papers_with_citations = [p for p in papers if p.get("citationCount") is not None]
    papers_sorted = sorted(papers_with_citations, key=lambda x: x["citationCount"], reverse=True)

    for paper_data in papers_sorted[:20]:
        paper = Paper(
            faculty_id=faculty.id,
            title=paper_data.get("title", "Untitled"),
            abstract=paper_data.get("abstract"),
            year=paper_data.get("year"),
            venue=paper_data.get("venue"),
            citation_count=paper_data.get("citationCount"),
        )
        db.add(paper)

    db.commit()
    print(f"  Saved {author['name']} ({school}) with {min(len(papers_sorted), 20)} papers")
    return faculty


def fetch_all_faculty():
    db = SessionLocal()
    total_count = sum(len(f) for f in FACULTY_BY_SCHOOL.values())
    processed = 0
    saved = 0
    failed = 0

    try:
        for school, faculty_list in FACULTY_BY_SCHOOL.items():
            print(f"\nProcessing: {school} ({len(faculty_list)} faculty)")

            for name in faculty_list:
                processed += 1
                print(f"[{processed}/{total_count}] {name}")

                search_result = search_author(name)
                if not search_result:
                    print(f"  Not found")
                    failed += 1
                    time.sleep(3)
                    continue

                author = get_author_details(search_result["authorId"])
                if not author:
                    failed += 1
                    time.sleep(3)
                    continue

                result = save_faculty(db, author, school)
                if result:
                    saved += 1

                time.sleep(3)

        print(f"\nDONE! Processed: {processed}, Saved: {saved}, Failed: {failed}")

    finally:
        db.close()


if __name__ == "__main__":
    fetch_all_faculty()
