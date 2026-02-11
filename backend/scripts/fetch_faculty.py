import os
import sys
import argparse
import requests
import time
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models import Faculty, Paper

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from economics_faculty import ECONOMICS_FACULTY
from biostat_faculty import BIOSTAT_FACULTY
from ds_expansion_faculty import DS_EXPANSION_FACULTY
from ee_faculty import EE_FACULTY
from materials_faculty import MATERIALS_FACULTY
from compbio_faculty import COMPBIO_FACULTY
from bme_faculty import BME_FACULTY
from chemeng_faculty import CHEMENG_FACULTY
from ucsb_faculty import UCSB_FACULTY
from ucla_faculty import UCLA_FACULTY
from stanford_faculty import STANFORD_FACULTY
from uci_faculty import UCI_FACULTY
from berkeley_faculty import BERKELEY_FACULTY
from ucsd_faculty import UCSD_FACULTY
from usc_faculty import USC_FACULTY
from caltech_faculty import CALTECH_FACULTY
from ucdavis_faculty import UCDAVIS_FACULTY
from sdsu_faculty import SDSU_FACULTY
from ucr_faculty import UCR_FACULTY
from ucsc_faculty import UCSC_FACULTY
from rutgers_faculty import RUTGERS_FACULTY
from utah_faculty import UTAH_FACULTY
from duke_faculty import DUKE_FACULTY

load_dotenv()

S2_API = "https://api.semanticscholar.org/graph/v1"
S2_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

HEADERS = {"x-api-key": S2_API_KEY} if S2_API_KEY else {}

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
    ],
    "UCI CS": [
        "Padhraic Smyth", "Alexander Ihler", "Sameer Singh", "Eric Mjolsness", "Pierre Baldi",
        "Xiaohui Xie", "Stephan Mandt", "Erik Sudderth", "Rina Dechter", "Michael Goodrich",
        "Dan Hirschberg", "David Eppstein", "Sandy Irani", "Vijay Vazirani", "Michael Franz",
        "Gene Tsudik", "Athina Markopoulou", "Marco Levorato", "Nalini Venkatasubramanian"
    ],
    "UCSB CS": [
        "William Wang", "Xifeng Yan", "Ambuj Singh", "Tao Yang", "Tevfik Bultan",
        "Ben Hardekopf", "Giovanni Vigna", "Christopher Kruegel", "Tim Sherwood", "Fred Chong",
        "Yuan Xie", "Yufei Ding", "Lei Li", "Shiyu Chang", "Yu-Xiang Wang",
        "Arpit Gupta", "Trinabh Gupta", "Jonathan Balkind"
    ]
}

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
    ],
    "UCI Stats": [
        "Hal Stern", "Wesley Johnson", "Michele Guindani", "Babak Shahbaba", "Daniel Gillen",
        "Vladimir Minin", "Bin Nan", "Yaming Yu", "Zhaoxia Yu", "Annie Qu",
        "Weining Shen", "Hernando Ombao"
    ],
    "UCSB Stats": [
        "S. Rao Jammalamadaka", "John Hsu", "Wendy Meiring", "Andrew Carter", "Sang-Yun Oh",
        "Michael Ludkovski", "Alexander Petersen", "Yuedong Wang", "Noel Cressie"
    ]
}

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
    ],
    "UCSB Applied Math": [
        "Bjorn Birnir", "Paul Atzberger", "Hector Ceniceros", "Carlos Garcia-Cervera",
        "Thomas Sideris", "Xu Yang", "Jean-Pierre Fouque", "Tomoyuki Ichiba"
    ]
}

MATH_GENERAL_FACULTY = {
    "MIT Math": [
        "Alexei Borodin", "Jacopo Borga", "Elchanan Mossel", "Philippe Rigollet",
        "Scott Sheffield", "Nike Sun"
    ],
    "Stanford Math": [
        "Daniel Bump", "Persi Diaconis", "Jacob Fox", "Sarah Peluse",
        "Kannan Soundararajan", "Jan Vondrák", "Sourav Chatterjee"
    ],
    "Berkeley Math": [
        "Bernd Sturmfels", "Lauren Williams", "Michael Christ", "Tatiana Toro",
        "James Sethian", "Martin Wainwright"
    ],
    "Princeton Math": [
        "Noga Alon", "Maria Chudnovsky", "Peter Constantin", "Charles Fefferman",
        "Igor Rodnianski", "Paul Seymour", "Allan Sly", "Elias Stein"
    ],
    "UChicago Math": [
        "László Babai", "Gregory Lawler", "Ewain Gwynne", "Alexander Razborov", "Amie Wilkinson"
    ],
    "Harvard Math": [
        "Laura DeMarco", "Denis Auroux", "Joe Harris", "Lauren Williams",
        "Mark Kisin", "Hiro Lee Tanaka"
    ],
    "Yale Math": [
        "Ronald Coifman", "Peter Jones", "Richard Kenyon", "Wilhelm Schlag",
        "Charles Smart", "Van Vu"
    ],
    "Columbia Math": [
        "Ivan Corwin", "Julien Dubedat", "Ioannis Karatzas", "Marcel Nutz",
        "Daniel Lacker", "Andrei Okounkov"
    ],
    "Cornell Math": [
        "Marcelo Aguiar", "Robert Connelly", "Allen Knutson", "Lionel Levine",
        "Karola Meszaros", "Edward Swartz", "Tara Holm"
    ],
    "NYU Courant Math": [
        "Gerard Ben Arous", "Paul Bourgade", "Percy Deift", "Sinan Gunturk",
        "Nina Holden", "Eyal Lubetzky", "Charles Newman", "S. R. Srinivasa Varadhan",
        "Ofer Zeitouni", "Sylvia Serfaty"
    ],
    "UCLA Math": [
        "Igor Pak", "Terence Tao", "Marek Biskup", "John Garnett",
        "Rowan Killip", "Sorin Popa", "Dimitri Shlyakhtenko", "Raphael Rouquier"
    ],
    "UMich Math": [
        "Jeff Lagarias", "Kartik Prasanna", "Mattias Jonsson", "Stephen DeBacker", "Karen Smith"
    ],
    "Wisconsin Math": [
        "David Anderson", "Hanbaek Lyu", "Hao Shen", "Benedek Valko",
        "Paul Terwilliger", "Botong Wang", "Timo Seppalainen"
    ],
    "UPenn Math": [
        "James Haglund", "Philip Gressman", "Ryan Hynd", "Yumeng Ou",
        "Robin Pemantle", "Robert Strain", "Jason Altschuler"
    ],
    "Duke Math": [
        "Nicholas Cook", "Alexander Dunlap", "Richard Durrett", "Jianfeng Lu",
        "Jonathan Mattingly", "James Nolen", "Ezra Miller", "Alexander Kiselev"
    ],
    "Northwestern Math": [
        "Xiumin Du", "Reza Gheissari", "Rachel Greenfeld", "Elton Hsu",
        "Marcus Michelen", "Bryna Kra", "Sandy Zabell"
    ],
    "Caltech Math": [
        "David Conlon", "Thomas Hutchcroft", "Nikolai Markarov", "Eric Rains",
        "Omer Tamuz", "Lingfu Zhang", "Matilde Marcolli"
    ],
    "Brown Math": [
        "Brendan Hassett", "Dan Abramovich", "Jill Pipher", "Brett Bernstein"
    ],
    "UT Austin Math": [
        "Luis Caffarelli", "Francesco Maggi", "Matias Delgadino", "Irene Gamba",
        "Maria Gualdani", "Arie Israel", "Alexis Vasseur"
    ],
    "CMU Math": [
        "Alan Frieze", "Tom Bohman", "Boris Bukh", "Po-Shen Loh",
        "Prasad Tetali", "Wesley Pegden"
    ]
}

PHYSICS_FACULTY = {
    "MIT Physics": [
        "Mehran Kardar", "Isaac Chuang", "William Oliver", "Aram Harrow",
        "Paola Cappellaro", "Liang Fu", "Max Metlitski", "Xiao-Gang Wen",
        "Leonid Mirny", "Jesse Thaler", "Max Tegmark", "Soonwon Choi"
    ],
    "Stanford Physics": [
        "Patrick Hayden", "Steven Kivelson", "Vedika Khemani", "Xiaoliang Qi",
        "Monika Schleier-Smith", "Shanhui Fan", "Jelena Vuckovic", "Ben Feldman"
    ],
    "Berkeley Physics": [
        "Hartmut Häffner", "Norman Yao", "Joel Moore", "Michael Zaletel",
        "Jeffrey Neaton", "Irfan Siddiqi", "Dung-Hai Lee", "Steven Louie"
    ],
    "Princeton Physics": [
        "Andrew Houck", "Jason Petta", "Herman Verlinde", "Silviu Pufu",
        "Jeff Thompson", "Ali Yazdani"
    ],
    "UChicago Physics": [
        "David Awschalom", "Cheng Chin", "Sidney Nagel", "Suriyanarayanan Vaikuntanathan",
        "Promit Ghosal"
    ],
    "Harvard Physics": [
        "Mikhail Lukin", "Ashvin Vishwanath", "Subir Sachdev", "Markus Greiner",
        "Efthimios Kaxiras", "Eugene Khalaf"
    ],
    "Yale Physics": [
        "Michel Devoret", "Robert Schoelkopf", "Steven Girvin", "Daisuke Nagai"
    ],
    "Columbia Physics": [
        "Andrew Millis", "Henry Yuen", "Dmitri Basov", "Abhay Pasupathy",
        "Sebastian Will", "Raquel Queiroz", "Dries Sels"
    ],
    "Cornell Physics": [
        "Eun-Ah Kim", "Paul McEuen", "Michelle Wang", "Nick Rivera"
    ],
    "Caltech Physics": [
        "John Preskill", "Alexei Kitaev", "Fernando Brandao", "Oskar Painter",
        "Manuel Endres", "Xie Chen"
    ],
    "UCLA Physics": [
        "Prineha Narang", "Alexander Balandin", "Yaroslav Tserkovnyak", "Eric Hudson"
    ],
    "UIUC Physics": [
        "Paul Kwiat", "Nadya Mason", "Karin Dahmen", "Dale Van Harlingen"
    ],
    "UMich Physics": [
        "Emanuel Gull", "Xiaoming Mao", "Sharon Glotzer", "Kai Sun", "Mark Newman"
    ],
    "UT Austin Physics": [
        "Scott Aaronson", "Elaine Li", "Allan MacDonald", "Nick Hunter-Jones"
    ],
    "Duke Physics": [
        "Matthew Hastings", "Harold Baranger", "Henry Greenside", "Travis Nicholson", "Huanqian Loh"
    ],
    "UW Physics": [
        "Boris Blinov", "Kai-Mei Fu", "Ting Cao"
    ],
    "UMD Physics": [
        "Chris Monroe", "Norbert Linke", "Victor Galitski", "Kartik Srinivasan"
    ],
    "Georgia Tech Physics": [
        "Predrag Cvitanovic", "Michael Chapman", "Colin Parker"
    ]
}

CS_GENERAL_FACULTY = {
    "MIT CS Theory/Systems": [
        "Frans Kaashoek", "Robert Morris", "Nickolai Zeldovich", "Adam Belay",
        "Henry Corrigan-Gibbs", "Vinod Vaikuntanathan", "Yael Kalai"
    ],
    "Stanford CS Theory/Systems": [
        "John Ousterhout", "Mendel Rosenblum", "Philip Levis", "Christos Kozyrakis",
        "Alex Aiken", "Mary Wootters", "Aaron Sidford"
    ],
    "Berkeley CS Theory/Systems": [
        "Sylvia Ratnasamy", "John Kubiatowicz", "Joseph Hellerstein", "Raluca Ada Popa",
        "Koushik Sen", "Max Willsey", "Alvin Cheung", "Christopher Fletcher"
    ],
    "CMU CS Theory/Systems": [
        "David Andersen", "Nathan Beckmann", "Phillip Gibbons", "Rashmi Vinayak",
        "Bryan Parno", "George Amvrosiadis", "Stephanie Balzer", "Maria Balcan"
    ],
    "Princeton CS Theory/Systems": [
        "Wyatt Lloyd", "Kyle Jamieson", "Ran Raz", "Huacheng Yu",
        "Zachary Kincaid"
    ],
    "Cornell CS Theory/Systems": [
        "Robbert van Renesse", "Nate Foster", "Dexter Kozen", "Robert Kleinberg",
        "Ken Birman", "Christopher Batten"
    ],
    "UW CS Theory/Systems": [
        "Tom Anderson", "Arvind Krishnamurthy", "Dan Grossman", "Zachary Tatlock",
        "Simon Peter", "Paul Beame", "Anna Karlin", "Shayan Oveis Gharan",
        "Mark Oskin", "Michael Bedford Taylor"
    ],
    "UT Austin CS Theory/Systems": [
        "Vijay Chidambaram", "Christopher Rossbach", "Emmett Witchel",
        "David Zuckerman", "Calvin Lin"
    ],
    "UIUC CS Theory/Systems": [
        "Grigore Rosu", "Madhusudan Parthasarathy", "Kevin Chang", "Bill Gropp", "Jeff Erickson"
    ],
    "Georgia Tech CS Theory/Systems": [
        "Alexandros Daglis", "Thomas Conte", "Umakishore Ramachandran"
    ],
    "UCLA CS Theory/Systems": [
        "Jens Palsberg", "Harry Xu", "Remy Wang"
    ],
    "UMich CS Theory/Systems": [
        "Satish Narayanasamy", "Yatin Manerkar", "George Tzimpragos",
        "Max New", "Cyrus Omar", "Manos Kapritsos"
    ],
    "Columbia CS Theory/Systems": [
        "Asaf Cidon", "Junfeng Yang", "Xi Chen"
    ],
    "Harvard CS Theory/Systems": [
        "Minlan Yu", "Juncheng Yang", "Madhu Sudan", "Boaz Barak", "Nada Amin"
    ],
    "Yale CS Theory/Systems": [
        "Bryan Ford", "Yang Richard Yang", "Avi Silberschatz"
    ],
    "Brown CS Theory/Systems": [
        "Tim Nelson", "Nikos Vasilakis", "Kathi Fisler", "Will Crichton"
    ],
    "UPenn CS Theory/Systems": [
        "Andre DeHon", "Joe Devietti", "Sebastian Angel", "Boon Thau Loo"
    ],
    "Duke CS Theory/Systems": [
        "Alvin Lebeck", "Landon Cox", "Bruce Maggs"
    ],
    "Northwestern CS Theory/Systems": [
        "Simone Campanoni", "Jason Hartline", "Aravindan Vijayaraghavan", "Sidhanth Mohanty"
    ],
    "Purdue CS Theory/Systems": [
        "Tiark Rompf", "Milind Kulkarni", "Samuel Midkiff", "Mithuna Thottethodi"
    ],
    "UCSD CS Theory/Systems": [
        "Hadi Esmaeilzadeh", "Jishen Zhao", "Ranjit Jhala"
    ],
    "UMass CS Theory/Systems": [
        "Arjun Guha", "Andrew McGregor"
    ],
    "UMD CS Theory/Systems": [
        "Michael Hicks", "Jeffrey Foster", "Neil Spring", "Samir Khuller"
    ],
    "Wisconsin CS Theory/Systems": [
        "Michael Swift", "Dileep Kini"
    ],
    "Caltech CS Theory/Systems": [
        "Urmila Mahadev", "John Ledyard"
    ]
}

INFORMATICS_FACULTY = {
    "Berkeley iSchool": [
        "David Bamman", "Joshua Blumenstock", "Marti Hearst", "Hany Farid",
        "Coye Cheshire", "Deirdre Mulligan", "Niloufar Salehi", "Steven Weber",
        "Alistair Croll", "AnHai Doan", "Morgan Ames", "Nick Merrill"
    ],
    "UMich SI": [
        "Christopher Brooks", "Ceren Budak", "Kevyn Collins-Thompson", "Abigail Jacobs",
        "David Jurgens", "Matthew Kay", "Paul Resnick", "Daniel Romero",
        "Sarita Schoenebeck", "Andrea Thomer", "Vinod Vydiswaran", "Libby Hemphill"
    ],
    "UW iSchool": [
        "Bill Howe", "Jevin West", "Anind K. Dey", "Amy J. Ko", "Tanu Mitra",
        "Katie Davis", "Cecilia Aragon", "Jacob O. Wobbrock", "Aylin Caliskan",
        "Ben Lee", "Martin Saveski", "Emma Spiro", "Melanie Walsh", "Nicholas Weber",
        "Lindah Kotut", "Lucy Lu Wang", "Chirag Shah", "Alexis Hiniker"
    ],
    "Cornell IS": [
        "Michael Macy", "Cristian Danescu-Niculescu-Mizil", "Shiri Azenkot",
        "Solon Barocas", "Larry Blume", "Cristobal Cheyre", "Tanzeem Choudhury",
        "Abe Davis", "Nicola Dell", "David Easley", "Deborah Estrin", "Nikhil Garg"
    ],
    "UIUC iSchool": [
        "Catherine Blake", "J. Stephen Downie", "Jingrui He", "Christopher Lueg",
        "Eunice E. Santos", "Ted Underwood", "Yang Wang", "Dong Wang", "Nigel Bosch",
        "Ryan Cordell", "Yun Huang", "Matthew Turk", "Vetle Torvik", "Kahyun Choi",
        "Yonghan Jung", "Jiaqi Ma", "Haohan Wang"
    ],
    "Maryland iSchool": [
        "Douglas Oard", "Joel Chan", "Vanessa Frias-Martinez", "Brian Butler",
        "Wei Ai", "Christopher Antoun", "Eun Kyoung Choe", "Hernisa Kacorri",
        "Jennifer Preece", "Ben Shneiderman"
    ],
    "UT Austin iSchool": [
        "Matthew Lease", "Ying Ding", "Jacek Gwizdka", "Elliott Hauser",
        "James Howison", "Chan Park", "Jiaxin Pei", "Nathan TeBlunthuis",
        "Yan Zhang", "Min Kyung Lee"
    ],
    "Indiana Luddy": [
        "Filippo Menczer", "David Wild", "Patrick Shih", "Karl MacDorman",
        "Andrew Miller", "Stephen Downs", "Samantha Wood", "Katy Börner",
        "Xiaozhong Liu", "Yong-Yeol Ahn"
    ],
    "UNC SILS": [
        "Diane Kelly", "Gary Marchionini", "Ryan Shaw", "Stephanie Haas",
        "Arcot Rajasekar", "Jeffrey Bardzell", "Ronald Bergquist", "Jaime Arguello",
        "Brad Hemminger", "Yongjun Zhu"
    ],
    "Syracuse iSchool": [
        "Bei Yu", "Jennifer Stromer-Galley", "Jeffrey Saltz", "Sevgi Erdogan",
        "Yiqi Li", "Kelvin King", "Md Tariqul Islam", "Jasmina Tacheva",
        "Steve Sawyer", "Kevin Crowston"
    ],
    "Rutgers SCI": [
        "Vivek K. Singh", "Eugene Lee", "Amelia Acker", "Ali Motamedi",
        "Marie Radford", "Dafna Lemish", "Michael Lesk", "Tefko Saracevic"
    ],
    "Drexel CCI": [
        "Jane Greenberg", "Xia Lin", "Erjia Yan", "Tim Gorichanaz",
        "Michelle Rogers", "Chaim Zins", "Jake Williams", "Yuan An"
    ]
}

CATEGORY_MAP = {
    "cs": CS_FACULTY,
    "stats": STATS_FACULTY,
    "ds": DS_FACULTY,
    "math": MATH_FACULTY,
    "math_general": MATH_GENERAL_FACULTY,
    "physics": PHYSICS_FACULTY,
    "cs_general": CS_GENERAL_FACULTY,
    "economics": ECONOMICS_FACULTY,
    "biostat": BIOSTAT_FACULTY,
    "ds_expansion": DS_EXPANSION_FACULTY,
    "ee": EE_FACULTY,
    "materials": MATERIALS_FACULTY,
    "compbio": COMPBIO_FACULTY,
    "bme": BME_FACULTY,
    "chemeng": CHEMENG_FACULTY,
    "ucsb": UCSB_FACULTY,
    "ucla": UCLA_FACULTY,
    "stanford": STANFORD_FACULTY,
    "uci": UCI_FACULTY,
    "berkeley": BERKELEY_FACULTY,
    "ucsd": UCSD_FACULTY,
    "usc": USC_FACULTY,
    "caltech": CALTECH_FACULTY,
    "ucdavis": UCDAVIS_FACULTY,
    "sdsu": SDSU_FACULTY,
    "ucr": UCR_FACULTY,
    "ucsc": UCSC_FACULTY,
    "rutgers": RUTGERS_FACULTY,
    "utah": UTAH_FACULTY,
    "duke": DUKE_FACULTY,
}

FACULTY_BY_SCHOOL = {}
FACULTY_BY_SCHOOL.update(CS_FACULTY)
FACULTY_BY_SCHOOL.update(STATS_FACULTY)
FACULTY_BY_SCHOOL.update(DS_FACULTY)
FACULTY_BY_SCHOOL.update(MATH_FACULTY)
FACULTY_BY_SCHOOL.update(MATH_GENERAL_FACULTY)
FACULTY_BY_SCHOOL.update(PHYSICS_FACULTY)
FACULTY_BY_SCHOOL.update(CS_GENERAL_FACULTY)
FACULTY_BY_SCHOOL.update(ECONOMICS_FACULTY)
FACULTY_BY_SCHOOL.update(BIOSTAT_FACULTY)
FACULTY_BY_SCHOOL.update(DS_EXPANSION_FACULTY)
FACULTY_BY_SCHOOL.update(EE_FACULTY)
FACULTY_BY_SCHOOL.update(MATERIALS_FACULTY)
FACULTY_BY_SCHOOL.update(COMPBIO_FACULTY)
FACULTY_BY_SCHOOL.update(BME_FACULTY)
FACULTY_BY_SCHOOL.update(CHEMENG_FACULTY)
FACULTY_BY_SCHOOL.update(UCSB_FACULTY)
FACULTY_BY_SCHOOL.update(UCLA_FACULTY)
FACULTY_BY_SCHOOL.update(STANFORD_FACULTY)
FACULTY_BY_SCHOOL.update(UCI_FACULTY)
FACULTY_BY_SCHOOL.update(BERKELEY_FACULTY)
FACULTY_BY_SCHOOL.update(UCSD_FACULTY)
FACULTY_BY_SCHOOL.update(USC_FACULTY)
FACULTY_BY_SCHOOL.update(CALTECH_FACULTY)
FACULTY_BY_SCHOOL.update(UCDAVIS_FACULTY)
FACULTY_BY_SCHOOL.update(SDSU_FACULTY)
FACULTY_BY_SCHOOL.update(UCR_FACULTY)
FACULTY_BY_SCHOOL.update(UCSC_FACULTY)
FACULTY_BY_SCHOOL.update(RUTGERS_FACULTY)
FACULTY_BY_SCHOOL.update(UTAH_FACULTY)
FACULTY_BY_SCHOOL.update(DUKE_FACULTY)


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


def fetch_all_faculty(categories: list[str] | None = None):
    """
    Fetch faculty from Semantic Scholar API.

    Args:
        categories: Optional list of category names to fetch (e.g., ['economics', 'biostat']).
                   If None, fetches all categories in FACULTY_BY_SCHOOL.
    """
    # Build the faculty dict based on categories filter
    if categories:
        faculty_to_fetch = {}
        for cat in categories:
            if cat not in CATEGORY_MAP:
                print(f"Warning: Unknown category '{cat}'. Available: {', '.join(CATEGORY_MAP.keys())}")
                continue
            faculty_to_fetch.update(CATEGORY_MAP[cat])
        if not faculty_to_fetch:
            print("No valid categories specified. Exiting.")
            return
    else:
        faculty_to_fetch = FACULTY_BY_SCHOOL

    db = SessionLocal()
    total_count = sum(len(f) for f in faculty_to_fetch.values())
    processed = 0
    saved = 0
    skipped = 0
    failed = 0

    print(f"\nFetching {total_count} faculty from {len(faculty_to_fetch)} schools/programs")
    if categories:
        print(f"Categories: {', '.join(categories)}")

    try:
        for school, faculty_list in faculty_to_fetch.items():
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
                    existing = db.query(Faculty).filter(
                        Faculty.semantic_scholar_id == author["authorId"]
                    ).first()
                    if existing and existing.id != result.id:
                        skipped += 1
                    else:
                        saved += 1

                time.sleep(3)

        print(f"\nDONE! Processed: {processed}, Saved: {saved}, Skipped (existing): {skipped}, Failed: {failed}")

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Fetch faculty data from Semantic Scholar API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available categories:
  {', '.join(CATEGORY_MAP.keys())}

Examples:
  # Fetch only economics and biostat faculty
  python -m scripts.fetch_faculty --only economics,biostat

  # Fetch new expansion categories
  python -m scripts.fetch_faculty --only economics,biostat,ds_expansion

  # List all categories and faculty counts
  python -m scripts.fetch_faculty --list

  # Fetch all faculty (default behavior)
  python -m scripts.fetch_faculty
"""
    )
    parser.add_argument(
        "--only",
        type=str,
        help="Comma-separated list of categories to fetch (e.g., 'economics,biostat,ds_expansion')"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available categories with faculty counts"
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable categories and faculty counts:")
        print("=" * 50)
        total = 0
        for cat, faculty_dict in CATEGORY_MAP.items():
            count = sum(len(f) for f in faculty_dict.values())
            schools = len(faculty_dict)
            total += count
            print(f"  {cat:15} {count:4} faculty across {schools:2} schools")
        print("=" * 50)
        print(f"  {'TOTAL':15} {total:4} faculty")
        return

    categories = None
    if args.only:
        categories = [c.strip() for c in args.only.split(",")]

    fetch_all_faculty(categories)


if __name__ == "__main__":
    main()
