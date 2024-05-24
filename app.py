from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import difflib

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS qa_pairs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT NOT NULL,
                  answer TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Insert predefined data into the database
def insert_predefined_data():
    predefined_data = [
        ("What is your name?", "I am a chatbot."),
        ("How are you?", "I am fine, thank you!"),
        ("What can you do?", "I can answer your questions."),
        ("What is Pakistan?", "Pakistan, officially the Islamic Republic of Pakistan is a country in South Asia. It is the fifth most populous country, with a population of over 241.5 million having the second-largest Muslim population as of 2023"),
        ("Where is Pakistan located?", "Pakistan is located in Southern Asia bordering the Arabian Sea, between India to the east and Iran and Afghanistan to the west and China to the north. Pakistan covers an area of 803,943 sq."),
        ("What is the capital of Pakistan?", "The capital of Pakistan is Islamabad."),
        ("What are the major cities in Pakistan?", "Some of the major cities in Pakistan include Karachi, Lahore, Islamabad, Rawalpindi, Faisalabad, and Multan."),
        ("What languages are spoken in Pakistan?", "The official language of Pakistan is Urdu, but other languages spoken include Punjabi, Pashto, Sindhi, Balochi, and Saraiki. English is also widely used in business and government."),
        ("What is the currency of Pakistan?", "The currency of Pakistan is the Pakistani Rupee, abbreviated as PKR."),
        ("What is the population of Pakistan?", "As of the latest estimates, Pakistan has a population of over 225 million people, making it the fifth-most populous country in the world."),
        ("What is the climate like in Pakistan?", "Pakistan has a varied climate, ranging from arid and semi-arid in the southern and central regions to temperate in the north. The country experiences four seasons: winter, spring, summer, and autumn."),
        ("What is the national animal of Pakistan?", "The national animal of Pakistan is the Markhor, a species of wild goat native to the mountainous regions of Central Asia."),
        ("What is the national bird of Pakistan?", "The national bird of Pakistan is the Chukar Partridge, a gamebird native to South Asia and the Middle East."),
        ("What is the national flower of Pakistan?", "The national flower of Pakistan is the Jasmine, specifically the Jasminum officinale variety."),
        ("What is the national tree of Pakistan?", "The national tree of Pakistan is the Deodar Cedar, a coniferous tree native to the Himalayas and other mountainous regions of South Asia."),
        ("What is the national sport of Pakistan?", "The national sport of Pakistan is field hockey."),
        ("What is the history of Pakistan?", "Pakistan has a rich history that dates back thousands of years, with civilizations such as the Indus Valley Civilization flourishing in the region."),
        ("What is the political system of Pakistan?", "Pakistan is a federal parliamentary democratic republic, with a President as the head of state and a Prime Minister as the head of government."),
        ("Who is the founder of Pakistan?", "Muhammad Ali Jinnah, also known as Quaid-e-Azam (Great Leader), is considered the founder of Pakistan."),
        ("What is the national anthem of Pakistan?", "The national anthem of Pakistan is Qaumi Taranah, which was written by Hafeez Jalandhari and composed by Ahmed Ghulamali Chagla."),
        ("What is the national flag of Pakistan?", "The national flag of Pakistan consists of a dark green field with a white vertical stripe on the left side, a white crescent moon, and a five-pointed star in the middle."),
        ("What is the national day of Pakistan?", "The national day of Pakistan is celebrated on March 23rd each year, commemorating the Lahore Resolution passed on March 23, 1940, which laid the groundwork for the creation of Pakistan."),
        ("What is the significance of the Lahore Resolution?", "The Lahore Resolution, also known as the Pakistan Resolution, called for the creation of independent states for Muslims in British India, leading to the eventual formation of Pakistan."),
        ("What is the significance of Pakistan Day?", "Pakistan Day commemorates the Lahore Resolution of 1940, which laid the foundation for the creation of Pakistan as a separate nation for Muslims of the Indian subcontinent."),
        ("What is the significance of Independence Day in Pakistan?", "Independence Day in Pakistan, celebrated on August 14th, marks the day when Pakistan gained independence from British rule in 1947."),
        ("What is the role of Pakistan in the world?", "Pakistan plays a significant role in regional and global affairs, particularly in South Asia and the Muslim world. It is known for its strategic location, nuclear capabilities, and contributions to peacekeeping missions."),
        ("What is the relationship between Pakistan and India?", "Pakistan and India have a complex relationship, characterized by historical conflicts, territorial disputes, and occasional attempts at peace and reconciliation. The two countries have fought several wars and continue to engage in diplomatic negotiations to address their differences."),
        ("What is the relationship between Pakistan and China?", "Pakistan and China enjoy a close and strategic relationship, often described as an 'all-weather friendship'. The two countries collaborate on various economic, military, and infrastructure projects through initiatives such as the China-Pakistan Economic Corridor (CPEC)."),
        ("What is the relationship between Pakistan and the United States?", "The relationship between Pakistan and the United States has been characterized by periods of cooperation and tension, particularly in the context of counterterrorism efforts and regional stability in South Asia."),
        
    ("Who was the founder of Pakistan?", "Muhammad Ali Jinnah, also known as Quaid-e-Azam, is the founder of Pakistan."),
    ("When was Pakistan founded?", "Pakistan was founded on August 14, 1947."),
    ("What was the Lahore Resolution?", "The Lahore Resolution was a formal political statement adopted by the All-India Muslim League in 1940, which called for independent states for Muslims in north-western and eastern zones of India."),
    ("Who was the first Prime Minister of Pakistan?", "Liaquat Ali Khan was the first Prime Minister of Pakistan."),
    ("What is the significance of the 1947 partition?", "The 1947 partition marked the division of British India into two independent dominions, India and Pakistan, leading to massive migration and communal violence."),
    ("What was the role of Allama Iqbal in Pakistan's creation?", "Allama Iqbal is credited with envisioning the idea of a separate Muslim state in India, which laid the ideological foundation for Pakistan."),
    ("What is the Two-Nation Theory?", "The Two-Nation Theory was the ideological basis for the creation of Pakistan, proposing that Muslims and Hindus were distinct nations with their own customs, religion, and traditions."),
    ("What was the first constitution of Pakistan?", "The first constitution of Pakistan was adopted in 1956."),
    ("What event led to the creation of Bangladesh?", "The Bangladesh Liberation War of 1971, which resulted in the secession of East Pakistan and the creation of Bangladesh."),
    ("What was the objective of the Simla Agreement?", "The Simla Agreement was signed between India and Pakistan in 1972, aiming to normalize relations and lay down the principles for future bilateral relations."),
    ("What is the importance of the 1965 Indo-Pak war?", "The 1965 Indo-Pak war was significant as it was the first major conflict between India and Pakistan over the Kashmir issue."),
    ("What is the significance of the Kargil War?", "The Kargil War of 1999 was a major conflict between India and Pakistan in the Kargil district of Kashmir, leading to heightened tensions and international diplomatic intervention."),
    ("Who was Benazir Bhutto?", "Benazir Bhutto was the first woman to head a democratic government in a majority Muslim nation, serving as Prime Minister of Pakistan."),
    ("What was Operation Gibraltar?", "Operation Gibraltar was a covert operation launched by Pakistan to infiltrate forces into Jammu and Kashmir to cause insurgency against Indian rule."),
    ("What is the importance of the 1973 Constitution of Pakistan?", "The 1973 Constitution is the current constitution of Pakistan, establishing the country as a federal parliamentary republic."),
    ("What are the main political parties in Pakistan?", "The main political parties in Pakistan include the Pakistan Tehreek-e-Insaf (PTI), Pakistan Muslim League (Nawaz) (PML-N), and Pakistan Peoples Party (PPP)."),
    ("Who was Zulfikar Ali Bhutto?", "Zulfikar Ali Bhutto was a Pakistani politician who served as the President and later the Prime Minister of Pakistan, and founded the Pakistan Peoples Party (PPP)."),
    ("What is the Green Revolution in Pakistan?", "The Green Revolution in Pakistan refers to the period in the 1960s and 1970s when the country experienced significant increases in agricultural production due to new technologies."),
    ("What role did Pakistan play in the Cold War?", "During the Cold War, Pakistan aligned itself with the United States and was a member of CENTO and SEATO, playing a strategic role in regional politics."),
    ("What was the impact of General Zia-ul-Haq's rule?", "General Zia-ul-Haq's rule from 1978 to 1988 was marked by the Islamization of Pakistan, with the implementation of Sharia law and significant military involvement in politics."),
    ("Who was the first female Prime Minister of Pakistan?", "Benazir Bhutto was the first female Prime Minister of Pakistan."),
    ("What is the significance of the Gwadar Port?", "Gwadar Port is a deep-sea port developed with Chinese assistance, which plays a crucial role in the China-Pakistan Economic Corridor (CPEC) and regional trade."),
    ("What is the China-Pakistan Economic Corridor (CPEC)?", "CPEC is a major infrastructure project aimed at improving connectivity between Pakistan and China, including investments in transportation, energy, and telecommunications."),
    ("What was the outcome of the 1971 war between India and Pakistan?", "The 1971 war resulted in the secession of East Pakistan and the creation of the independent state of Bangladesh."),
    ("Who was General Pervez Musharraf?", "General Pervez Musharraf was the military ruler of Pakistan who took power in a coup in 1999 and served as President until 2008."),
    ("What was the Lal Masjid Operation?", "The Lal Masjid Operation in 2007 was a military operation against the Lal Masjid mosque in Islamabad, which had become a center of militant activity."),
    ("What is the importance of the Karachi Agreement of 1949?", "The Karachi Agreement of 1949 was a ceasefire agreement between India and Pakistan, brokered by the United Nations, to address the Kashmir conflict."),
    ("What was the role of Pakistan in the Afghan War of the 1980s?", "Pakistan played a key role in supporting the Afghan Mujahideen against the Soviet invasion, with significant assistance from the United States and Saudi Arabia."),
    ("What was the Kargil conflict?", "The Kargil conflict in 1999 was a limited war between India and Pakistan in the Kargil district of Kashmir."),
    ("What is the strategic significance of the Gwadar Port?", "Gwadar Port's strategic significance lies in its location near the Strait of Hormuz, a key maritime route for global oil supplies."),
    ("What are the key features of the Indus Waters Treaty?", "The Indus Waters Treaty is a water-sharing agreement between India and Pakistan, brokered by the World Bank in 1960, which allocates the use of the Indus River and its tributaries."),
    ("What was the significance of the 1965 War?", "The 1965 War was the first major conflict between India and Pakistan over the Kashmir issue, leading to significant military engagements and international mediation."),
    ("Who was Liaquat Ali Khan?", "Liaquat Ali Khan was the first Prime Minister of Pakistan and a close aide of Muhammad Ali Jinnah."),
    ("What was the Balochistan insurgency?", "The Balochistan insurgency refers to several armed uprisings by Baloch nationalists in Pakistan's Balochistan province, seeking greater autonomy or independence."),
    ("What role did Pakistan play in the War on Terror?", "Pakistan has been a key ally in the War on Terror, cooperating with the United States in counterterrorism operations and facing internal challenges from militant groups."),
    ("What is the importance of the Khyber Pass?", "The Khyber Pass is a strategic mountain pass connecting Pakistan and Afghanistan, historically significant for trade and military invasions."),
    ("Who was Nawaz Sharif?", "Nawaz Sharif is a Pakistani politician who has served as Prime Minister multiple times, representing the Pakistan Muslim League (Nawaz) party."),
    ("What is the significance of the 1998 nuclear tests?", "The 1998 nuclear tests conducted by Pakistan demonstrated its nuclear capabilities and established it as a nuclear-armed state."),
    ("What is the role of the Inter-Services Intelligence (ISI)?", "The ISI is Pakistan's premier intelligence agency, playing a significant role in national security, counterintelligence, and covert operations."),
    ("What was the role of the All-India Muslim League?", "The All-India Muslim League was the political party that led the movement for the creation of Pakistan, under the leadership of Muhammad Ali Jinnah."),
    ("What was the impact of the 2005 earthquake in Pakistan?", "The 2005 earthquake caused widespread devastation in northern Pakistan, leading to significant loss of life and prompting international humanitarian aid."),
    ("What is the historical significance of Mohenjo-daro?", "Mohenjo-daro is an ancient city of the Indus Valley Civilization, one of the world's earliest urban settlements, located in present-day Pakistan."),
    ("Who was Fatima Jinnah?", "Fatima Jinnah was a Pakistani dental surgeon, biographer, stateswoman, and one of the leading founders of Pakistan, known as the 'Mother of the Nation'."),
    ("What is the significance of the Mangla Dam?", "The Mangla Dam, built on the Jhelum River, is one of Pakistan's largest dams, crucial for water storage and hydroelectric power generation."),
    ("What was the impact of Zulfikar Ali Bhutto's nationalization policy?", "Zulfikar Ali Bhutto's nationalization policy in the 1970s aimed to transfer major industries and banks to state ownership, impacting the economy significantly."),
    ("Who was General Yahya Khan?", "General Yahya Khan was a Pakistani military ruler who served as President from 1969 to 1971, during the Bangladesh Liberation War."),
    ("What is the significance of the Chagai Hills?", "The Chagai Hills in Balochistan are the site of Pakistan's nuclear tests conducted in 1998."),
    ("What was the role of Pakistan in the United Nations peacekeeping missions?", "Pakistan has been one of the largest contributors to UN peacekeeping missions, participating in various operations around the world."),
    ("What is the historical importance of Taxila?", "Taxila is an ancient city in Pakistan, known for its archaeological significance and its role as a center of learning in ancient times."),
    ("What was the role of the Khilafat Movement?", "The Khilafat Movement was a pan-Islamic political campaign in British India, supporting the Ottoman Caliphate and opposing British rule, which had a significant impact on Indian Muslims."),
    ("What was the impact of the Radcliffe Line?", "The Radcliffe Line was the boundary demarcation line between India and Pakistan upon partition in 1947, leading to significant migration and communal violence."),
    ("What was the significance of the 1956 Constitution?", "The 1956 Constitution was the first constitution of Pakistan, declaring it an Islamic republic and setting the framework for its governance."),
    ("What is the significance of the Khyber Pakhtunkhwa province?", "Khyber Pakhtunkhwa (formerly NWFP) is a province in Pakistan known for its strategic location, cultural heritage, and role in regional geopolitics."),
    ("What was the role of the All Parties Hurriyat Conference?", "The All Parties Hurriyat Conference is an alliance of pro-freedom parties in Jammu and Kashmir, advocating for the right to self-determination."),
    ("What was the impact of the 1977 military coup?", "The 1977 military coup led by General Zia-ul-Haq overthrew Prime Minister Zulfikar Ali Bhutto, resulting in martial law and significant political changes in Pakistan."),
    ("Who was Malala Yousafzai?", "Malala Yousafzai is a Pakistani education activist and the youngest-ever Nobel Prize laureate, known for her advocacy of girls' education."),
    ("What was the Rann of Kutch dispute?", "The Rann of Kutch dispute was a territorial conflict between India and Pakistan in 1965 over the salt marsh region in Gujarat, leading to military skirmishes."),
    ("What is the significance of the 1984 Operation Meghdoot?", "Operation Meghdoot was an Indian military operation to capture the Siachen Glacier in the disputed Kashmir region, leading to ongoing territorial disputes with Pakistan."),
    ("What is the role of the Pakistan Armed Forces?", "The Pakistan Armed Forces play a significant role in the country's defense, national security, and international peacekeeping efforts."),
    ("What was the impact of the 2007 Lal Masjid siege?", "The 2007 Lal Masjid siege was a military operation against a militant mosque in Islamabad, leading to significant casualties and highlighting the issue of extremism in Pakistan."),
    ("What was the role of Pakistan in the Gulf War?", "During the Gulf War, Pakistan provided support to the US-led coalition and contributed troops to protect Saudi Arabia's holy sites."),
    ("What is the significance of the Islamabad Capital Territory?", "Islamabad Capital Territory is the region encompassing Pakistan's capital city, Islamabad, and is the political and administrative center of the country."),
    ("What was the impact of the 2010 floods in Pakistan?", "The 2010 floods in Pakistan were among the worst natural disasters in the country's history, causing widespread damage, displacement, and a humanitarian crisis."),
    ("What was the role of the Pakistan Movement?", "The Pakistan Movement was the political effort led by the All-India Muslim League to create an independent Muslim state, resulting in the establishment of Pakistan in 1947."),
    ("What was the significance of the 1962 Sino-Indian War for Pakistan?", "The 1962 Sino-Indian War led to improved relations between Pakistan and China, as both countries sought to counterbalance India."),
    ("What was the role of Ayub Khan in Pakistan's history?", "Ayub Khan was Pakistan's military ruler from 1958 to 1969, known for his modernization efforts and the introduction of a new constitution in 1962."),
    ("What is the significance of the Orakzai Agency?", "The Orakzai Agency is one of the tribal areas in Pakistan, known for its strategic importance and history of militant activity."),
    ("What was the impact of the Afghan Refugee Crisis on Pakistan?", "The Afghan Refugee Crisis brought millions of Afghan refugees to Pakistan during the Soviet-Afghan War, impacting the country's social and economic landscape."),
    ("What is the role of the Pakistan Navy?", "The Pakistan Navy is responsible for the defense of Pakistan's maritime interests and has played a crucial role in regional security and anti-piracy operations."),
    ("What was the impact of the 2001 Indian Parliament attack on Pakistan-India relations?", "The 2001 Indian Parliament attack led to heightened tensions and military standoff between India and Pakistan, affecting bilateral relations."),
    ("What is the historical significance of the Kalash Valley?", "The Kalash Valley is known for its unique cultural heritage and the indigenous Kalash people, who have distinct traditions and beliefs."),
    ("What was the impact of the 2014 Peshawar school attack?", "The 2014 Peshawar school attack was a terrorist attack on an army-run school, resulting in the deaths of over 140 people, mostly children, and leading to a major crackdown on terrorism."),
    ("What was the role of the Tehreek-e-Taliban Pakistan (TTP)?", "The Tehreek-e-Taliban Pakistan is a militant organization responsible for numerous terrorist attacks in Pakistan, advocating for the implementation of strict Sharia law."),
    ("What is the significance of the 1960 Indus Waters Treaty?", "The Indus Waters Treaty is a water-sharing agreement between India and Pakistan, facilitating cooperative management of shared river resources."),
    ("What was the impact of the 1979 Iranian Revolution on Pakistan?", "The 1979 Iranian Revolution influenced Pakistan's Shia population and impacted regional geopolitics, leading to increased sectarian tensions."),
    ("What was the role of the Kashmir conflict in Pakistan's history?", "The Kashmir conflict has been a central issue in Pakistan-India relations, leading to multiple wars and ongoing territorial disputes."),
    ("What is the significance of the Chitral region?", "Chitral is a mountainous region in northern Pakistan, known for its cultural heritage, scenic beauty, and strategic importance."),
    ("What was the impact of the 1999 military coup?", "The 1999 military coup led by General Pervez Musharraf overthrew Prime Minister Nawaz Sharif, resulting in military rule and significant political changes."),
    ("What is the role of the Pakistan Air Force?", "The Pakistan Air Force is responsible for the aerial defense of Pakistan, playing a key role in national security and regional stability."),
    ("What was the significance of the 1948 Indo-Pak war?", "The 1948 Indo-Pak war was the first conflict between India and Pakistan over Kashmir, leading to the establishment of the Line of Control."),
    ("What was the impact of the 2008 Mumbai attacks on Pakistan-India relations?", "The 2008 Mumbai attacks led to severe strain in Pakistan-India relations, with India accusing Pakistani-based militants of involvement."),
    ("What is the significance of the Balochistan province?", "Balochistan is Pakistan's largest province by area, known for its natural resources, strategic location, and ongoing insurgency issues."),
    ("What was the role of Pakistan in the Islamic world?", "Pakistan has played a significant role in the Islamic world, being a founding member of the Organization of Islamic Cooperation (OIC) and advocating for Muslim solidarity."),
    ("What is the significance of the 1972 Simla Agreement?", "The Simla Agreement aimed to normalize relations between India and Pakistan post-1971 war and establish the Line of Control in Kashmir."),
    ("What was the impact of the Soviet-Afghan War on Pakistan?", "The Soviet-Afghan War led to an influx of Afghan refugees into Pakistan and significant military and economic aid from the United States."),
    ("What is the role of the Federally Administered Tribal Areas (FATA)?", "FATA, now merged with Khyber Pakhtunkhwa, was a semi-autonomous tribal region in Pakistan, known for its unique governance and security challenges."),
    ("What was the impact of the 1974 Lahore Declaration?", "The 1974 Lahore Declaration was an agreement between India and Pakistan to foster peaceful relations and avoid conflict."),
    ("What is the significance of the Arabian Sea for Pakistan?", "The Arabian Sea provides Pakistan with vital maritime access for trade, naval operations, and strategic interests."),
    ("What was the role of the Pakistan Steel Mills?", "The Pakistan Steel Mills was established to develop the country's steel industry and reduce reliance on imports."),
    ("What is the significance of the 1958 martial law?", "The 1958 martial law marked the beginning of military rule in Pakistan, with General Ayub Khan taking over the government."),
    ("What was the impact of the 1962 Constitution?", "The 1962 Constitution introduced by Ayub Khan established a presidential system of government and centralized authority."),
    ("What is the role of the Pakistan National Assembly?", "The National Assembly is the lower house of Pakistan's bicameral parliament, responsible for legislation and representing the people."),
    ("What was the significance of the 1971 Bangladesh Liberation War?", "The 1971 Bangladesh Liberation War led to the secession of East Pakistan and the creation of the independent state of Bangladesh."),
    ("What is the historical significance of the Harappa site?", "Harappa is an archaeological site of the Indus Valley Civilization, providing insights into one of the world's earliest urban cultures."),
    ("What was the role of the 1965 Tashkent Agreement?", "The Tashkent Agreement was a peace accord between India and Pakistan to end hostilities following the 1965 war."),
    ("What is the significance of the Pakistan Movement Resolution of 1940?", "The Pakistan Movement Resolution of 1940, also known as the Lahore Resolution, called for the creation of independent states for Muslims in India, leading to the establishment of Pakistan."),
    ("What was the impact of the 2007 state of emergency in Pakistan?", "The 2007 state of emergency declared by President Pervez Musharraf led to the suspension of the constitution, widespread protests, and eventual political changes."),
    ("What is the role of the Pakistan Tehreek-e-Insaf (PTI)?", "The PTI is a major political party in Pakistan, founded by Imran Khan, advocating for anti-corruption measures and social justice."),
    ("What was the significance of the 1988 Benazir Bhutto election?", "The 1988 election marked the return of democracy in Pakistan and Benazir Bhutto becoming the first female Prime Minister of a Muslim-majority country."),
    ("What is the historical importance of the city of Lahore?", "Lahore is a historical city in Pakistan, known for its cultural heritage, Mughal architecture, and role in the Pakistan Movement."),
    ("What was the impact of the 2002 general elections in Pakistan?", "The 2002 general elections marked the return to civilian rule after military governance under Pervez Musharraf, with significant political realignment."),
    ("What is the role of the Inter-Services Public Relations (ISPR)?", "The ISPR is the media and public relations wing of the Pakistan Armed Forces, responsible for information dissemination and image management."),
    ("What was the significance of the 1990 Gulf War for Pakistan?", "During the 1990 Gulf War, Pakistan contributed troops to protect Saudi Arabia's holy sites and supported the US-led coalition."),
    ("What is the historical importance of the city of Karachi?", "Karachi is Pakistan's largest city and economic hub, known for its port, diverse population, and role in the independence movement."),
    ("What was the impact of the 1993 Prime Ministerial election?", "The 1993 election resulted in Benazir Bhutto's return to power, marking a period of political instability and economic challenges."),
    ("What is the role of the Pakistan Senate?", "The Senate is the upper house of Pakistan's bicameral parliament, representing the provinces and playing a key role in legislation."),
    ("What was the significance of the 1999 Kargil conflict?", "The Kargil conflict was a military confrontation between India and Pakistan in the Kargil district of Kashmir, leading to heightened tensions and international diplomatic efforts."),
    ("What is the historical significance of the city of Quetta?", "Quetta is the capital of Balochistan province, known for its strategic location, military presence, and role in regional geopolitics."),
    ("What was the impact of the 2008 general elections in Pakistan?", "The 2008 general elections marked the return to civilian rule after military governance under Pervez Musharraf, with the Pakistan Peoples Party winning a significant victory."),
    ("What is the role of the Pakistan Atomic Energy Commission (PAEC)?", "The PAEC is responsible for Pakistan's nuclear energy program, including power generation, research, and nuclear weapons development."),
    ("What was the significance of the 1974 Indian nuclear test for Pakistan?", "The 1974 Indian nuclear test prompted Pakistan to accelerate its own nuclear weapons program, leading to regional nuclear arms competition."),
    ("What is the historical importance of the city of Peshawar?", "Peshawar is a historical city in Pakistan, known for its ancient trade routes, cultural heritage, and strategic location near the Khyber Pass."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    ("What is the role of the Pakistan Rangers?", "The Pakistan Rangers are a paramilitary force responsible for maintaining law and order, particularly in border regions and urban areas."),
    ("What was the significance of the 1997 Pakistan-China border agreement?", "The 1997 border agreement between Pakistan and China formalized the demarcation of their shared border, strengthening bilateral relations."),
    ("What is the historical significance of the city of Multan?", "Multan is an ancient city in Pakistan, known for its Sufi shrines, historical monuments, and role in trade and commerce."),
    ("What was the impact of the 2018 general elections in Pakistan?", "The 2018 general elections resulted in the victory of Imran Khan's PTI, marking a significant shift in Pakistan's political landscape."),
    ("What is the role of the Pakistan Coast Guards?", "The Pakistan Coast Guards are responsible for protecting Pakistan's maritime borders, combating smuggling, and ensuring coastal security."),
    ("What was the significance of the 1960 water-sharing agreement with India?", "The 1960 Indus Waters Treaty between India and Pakistan facilitated the cooperative management of shared river resources, ensuring water security for both countries."),
    ("What is the historical importance of the city of Hyderabad?", "Hyderabad is a city in Sindh province, known for its cultural heritage, historical monuments, and role in the independence movement."),
    ("What was the impact of the 2007 Pakistan judiciary crisis?", "The 2007 judiciary crisis in Pakistan, triggered by the dismissal of Chief Justice Iftikhar Chaudhry, led to widespread protests and significant political upheaval."),
    ("What is the role of the Pakistan Frontier Corps?", "The Pakistan Frontier Corps are a paramilitary force responsible for border security, counterinsurgency, and maintaining law and order in the tribal areas."),
    ("What was the significance of the 1989 withdrawal of Soviet troops from Afghanistan for Pakistan?", "The withdrawal of Soviet troops from Afghanistan in 1989 ended a decade-long conflict, leading to the return of Afghan refugees and significant geopolitical shifts in the region."),
    ("What is the historical significance of the city of Faisalabad?", "Faisalabad, formerly known as Lyallpur, is an industrial city in Pakistan, known for its textile industry and economic importance."),
    ("What was the impact of the 2011 Osama bin Laden operation on Pakistan?", "The 2011 operation by US forces to kill Osama bin Laden in Abbottabad, Pakistan, led to strained US-Pakistan relations and raised questions about Pakistan's sovereignty and intelligence capabilities."),
    ("What is the role of the Pakistan Maritime Security Agency (PMSA)?", "The PMSA is responsible for enforcing maritime law, protecting Pakistan's maritime interests, and conducting search and rescue operations."),
    ("What was the significance of the 2006 Balochistan conflict?", "The 2006 conflict in Balochistan involved clashes between Baloch nationalists and Pakistani security forces, highlighting issues of autonomy and resource distribution."),
    ("What is the historical importance of the city of Rawalpindi?", "Rawalpindi is a major city in Pakistan, known for its military headquarters, strategic location, and historical significance."),
    ("What was the impact of the 2014 Operation Zarb-e-Azb?", "Operation Zarb-e-Azb was a military operation launched by Pakistan against militant groups in North Waziristan, leading to significant security improvements."),
    ("What is the role of the Pakistan International Airlines (PIA)?", "PIA is the national airline of Pakistan, providing domestic and international air travel services and playing a key role in the country's transportation sector."),
    ("What was the significance of the 1964 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1964 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Sialkot?", "Sialkot is an industrial city in Pakistan, known for its production of sports goods, surgical instruments, and its role in the independence movement."),
    ("What was the impact of the 2008 economic crisis on Pakistan?", "The 2008 global economic crisis led to significant economic challenges for Pakistan, including inflation, energy shortages, and a balance of payments crisis."),
    ("What is the role of the Pakistan Railways?", "Pakistan Railways is the state-owned railway company, providing transportation of passengers and goods across the country and playing a crucial role in the economy."),
    ("What was the significance of the 1977 military coup for Pakistan?", "The 1977 military coup led by General Zia-ul-Haq overthrew Prime Minister Zulfikar Ali Bhutto, resulting in martial law and significant political changes."),
    ("What is the historical importance of the city of Gujranwala?", "Gujranwala is an industrial city in Pakistan, known for its production of agricultural and industrial goods and its role in the independence movement."),
    ("What was the impact of the 1998 nuclear tests on Pakistan's international relations?", "The 1998 nuclear tests conducted by Pakistan established it as a nuclear-armed state, leading to international sanctions and significant changes in regional security dynamics."),
    ("What is the role of the Pakistan National Shipping Corporation (PNSC)?", "The PNSC is responsible for providing maritime transportation services, managing the national fleet, and playing a key role in Pakistan's trade and logistics."),
    ("What was the significance of the 1949 Karachi Agreement?", "The Karachi Agreement of 1949 was a ceasefire agreement between India and Pakistan, brokered by the United Nations, to address the Kashmir conflict."),
    ("What is the historical significance of the city of Bahawalpur?", "Bahawalpur is a historical city in Pakistan, known for its royal heritage, palaces, and role in the independence movement."),
    ("What was the impact of the 2013 Peshawar church bombing?", "The 2013 Peshawar church bombing was a terrorist attack targeting a Christian community, leading to significant casualties and highlighting issues of religious extremism."),
    ("What is the role of the Pakistan Broadcasting Corporation (PBC)?", "The PBC is responsible for public radio broadcasting in Pakistan, providing news, entertainment, and educational programs to the public."),
    ("What was the significance of the 2014 APS attack in Peshawar?", "The 2014 APS attack in Peshawar was a terrorist attack on a school, resulting in the deaths of over 140 people, mostly children, and leading to a major crackdown on terrorism."),
    ("What is the historical importance of the city of Sargodha?", "Sargodha is a city in Pakistan, known for its agricultural production, particularly citrus fruits, and its role in the independence movement."),
    ("What was the impact of the 1979 Iranian Revolution on Pakistan?", "The 1979 Iranian Revolution influenced Pakistan's Shia population and impacted regional geopolitics, leading to increased sectarian tensions."),
    ("What is the role of the Pakistan Civil Aviation Authority (PCAA)?", "The PCAA is responsible for regulating and overseeing civil aviation activities in Pakistan, ensuring safety, and managing airports."),
    ("What was the significance of the 1965 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1965 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Quetta?", "Quetta is the capital of Balochistan province, known for its strategic location, military presence, and role in regional geopolitics."),
    ("What was the impact of the 2014 military operation Zarb-e-Azb?", "Operation Zarb-e-Azb was a military operation launched by Pakistan against militant groups in North Waziristan, leading to significant security improvements."),
    ("What is the role of the Pakistan Rangers?", "The Pakistan Rangers are a paramilitary force responsible for maintaining law and order, particularly in border regions and urban areas."),
    ("What was the significance of the 2016 Quetta hospital bombing?", "The 2016 Quetta hospital bombing was a terrorist attack targeting a gathering of lawyers, resulting in significant casualties and highlighting issues of security."),
    ("What is the historical significance of the city of Multan?", "Multan is an ancient city in Pakistan, known for its Sufi shrines, historical monuments, and role in trade and commerce."),
    ("What was the impact of the 2008 economic crisis on Pakistan?", "The 2008 global economic crisis led to significant economic challenges for Pakistan, including inflation, energy shortages, and a balance of payments crisis."),
    ("What is the role of the Pakistan Coast Guards?", "The Pakistan Coast Guards are responsible for protecting Pakistan's maritime borders, combating smuggling, and ensuring coastal security."),
    ("What was the significance of the 1964 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1964 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Sialkot?", "Sialkot is an industrial city in Pakistan, known for its production of sports goods, surgical instruments, and its role in the independence movement."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    ("What is the role of the Pakistan Air Force?", "The Pakistan Air Force is responsible for the aerial defense of Pakistan, playing a key role in national security and regional stability."),
    ("What was the significance of the 1990 Gulf War for Pakistan?", "During the 1990 Gulf War, Pakistan contributed troops to protect Saudi Arabia's holy sites and supported the US-led coalition."),
    ("What is the historical significance of the city of Karachi?", "Karachi is Pakistan's largest city and economic hub, known for its port, diverse population, and role in the independence movement."),
    ("What was the impact of the 2018 general elections in Pakistan?", "The 2018 general elections resulted in the victory of Imran Khan's PTI, marking a significant shift in Pakistan's political landscape."),
    ("What is the role of the Pakistan Frontier Corps?", "The Pakistan Frontier Corps are a paramilitary force responsible for border security, counterinsurgency, and maintaining law and order in the tribal areas."),
    ("What was the significance of the 2006 Balochistan conflict?", "The 2006 conflict in Balochistan involved clashes between Baloch nationalists and Pakistani security forces, highlighting issues of autonomy and resource distribution."),
    ("What is the historical importance of the city of Faisalabad?", "Faisalabad, formerly known as Lyallpur, is an industrial city in Pakistan, known for its textile industry and economic importance."),
    ("What was the impact of the 2011 Osama bin Laden operation on Pakistan?", "The 2011 operation by US forces to kill Osama bin Laden in Abbottabad, Pakistan, led to strained US-Pakistan relations and raised questions about Pakistan's sovereignty and intelligence capabilities."),
    ("What is the role of the Pakistan Maritime Security Agency (PMSA)?", "The PMSA is responsible for enforcing maritime law, protecting Pakistan's maritime interests, and conducting search and rescue operations."),
    ("What was the significance of the 1998 nuclear tests on Pakistan's international relations?", "The 1998 nuclear tests conducted by Pakistan established it as a nuclear-armed state, leading to international sanctions and significant changes in regional security dynamics."),
    ("What is the role of the Pakistan National Shipping Corporation (PNSC)?", "The PNSC is responsible for providing maritime transportation services, managing the national fleet, and playing a key role in Pakistan's trade and logistics."),
    ("What was the significance of the 1971 Bangladesh Liberation War?", "The 1971 Bangladesh Liberation War led to the secession of East Pakistan and the creation of the independent state of Bangladesh."),
    ("What is the historical importance of the city of Hyderabad?", "Hyderabad is a city in Sindh province, known for its cultural heritage, historical monuments, and role in the independence movement."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    ("What is the role of the Pakistan Broadcasting Corporation (PBC)?", "The PBC is responsible for public radio broadcasting in Pakistan, providing news, entertainment, and educational programs to the public."),
    ("What was the significance of the 2014 APS attack in Peshawar?", "The 2014 APS attack in Peshawar was a terrorist attack on a school, resulting in the deaths of over 140 people, mostly children, and leading to a major crackdown on terrorism."),
    ("What is the historical importance of the city of Sargodha?", "Sargodha is a city in Pakistan, known for its agricultural production, particularly citrus fruits, and its role in the independence movement."),
    ("What was the impact of the 1979 Iranian Revolution on Pakistan?", "The 1979 Iranian Revolution influenced Pakistan's Shia population and impacted regional geopolitics, leading to increased sectarian tensions."),
    ("What is the role of the Pakistan Civil Aviation Authority (PCAA)?", "The PCAA is responsible for regulating and overseeing civil aviation activities in Pakistan, ensuring safety, and managing airports."),
    ("What was the significance of the 1965 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1965 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Quetta?", "Quetta is the capital of Balochistan province, known for its strategic location, military presence, and role in regional geopolitics."),
    ("What was the impact of the 2014 military operation Zarb-e-Azb?", "Operation Zarb-e-Azb was a military operation launched by Pakistan against militant groups in North Waziristan, leading to significant security improvements."),
    ("What is the role of the Pakistan Rangers?", "The Pakistan Rangers are a paramilitary force responsible for maintaining law and order, particularly in border regions and urban areas."),
    ("What was the significance of the 2016 Quetta hospital bombing?", "The 2016 Quetta hospital bombing was a terrorist attack targeting a gathering of lawyers, resulting in significant casualties and highlighting issues of security."),
    ("What is the historical significance of the city of Multan?", "Multan is an ancient city in Pakistan, known for its Sufi shrines, historical monuments, and role in trade and commerce."),
    ("What was the impact of the 2008 economic crisis on Pakistan?", "The 2008 global economic crisis led to significant economic challenges for Pakistan, including inflation, energy shortages, and a balance of payments crisis."),
    ("What is the role of the Pakistan Coast Guards?", "The Pakistan Coast Guards are responsible for protecting Pakistan's maritime borders, combating smuggling, and ensuring coastal security."),
    ("What was the significance of the 1964 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1964 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Sialkot?", "Sialkot is an industrial city in Pakistan, known for its production of sports goods, surgical instruments, and its role in the independence movement."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    ("What is the role of the Pakistan Air Force?", "The Pakistan Air Force is responsible for the aerial defense of Pakistan, playing a key role in national security and regional stability."),
    ("What was the significance of the 1990 Gulf War for Pakistan?", "During the 1990 Gulf War, Pakistan contributed troops to protect Saudi Arabia's holy sites and supported the US-led coalition."),
    ("What is the historical significance of the city of Karachi?", "Karachi is Pakistan's largest city and economic hub, known for its port, diverse population, and role in the independence movement."),
    ("What was the impact of the 2018 general elections in Pakistan?", "The 2018 general elections resulted in the victory of Imran Khan's PTI, marking a significant shift in Pakistan's political landscape."),
    ("What is the role of the Pakistan Frontier Corps?", "The Pakistan Frontier Corps are a paramilitary force responsible for border security, counterinsurgency, and maintaining law and order in the tribal areas."),
    ("What was the significance of the 2006 Balochistan conflict?", "The 2006 conflict in Balochistan involved clashes between Baloch nationalists and Pakistani security forces, highlighting issues of autonomy and resource distribution."),
    ("What is the historical importance of the city of Faisalabad?", "Faisalabad, formerly known as Lyallpur, is an industrial city in Pakistan, known for its textile industry and economic importance."),
    ("What was the impact of the 2011 Osama bin Laden operation on Pakistan?", "The 2011 operation by US forces to kill Osama bin Laden in Abbottabad, Pakistan, led to strained US-Pakistan relations and raised questions about Pakistan's sovereignty and intelligence capabilities."),
    ("What is the role of the Pakistan Maritime Security Agency (PMSA)?", "The PMSA is responsible for enforcing maritime law, protecting Pakistan's maritime interests, and conducting search and rescue operations."),
    ("What was the significance of the 1998 nuclear tests on Pakistan's international relations?", "The 1998 nuclear tests conducted by Pakistan established it as a nuclear-armed state, leading to international sanctions and significant changes in regional security dynamics."),
    ("What is the role of the Pakistan National Shipping Corporation (PNSC)?", "The PNSC is responsible for providing maritime transportation services, managing the national fleet, and playing a key role in Pakistan's trade and logistics."),
    ("What was the significance of the 1971 Bangladesh Liberation War?", "The 1971 Bangladesh Liberation War led to the secession of East Pakistan and the creation of the independent state of Bangladesh."),
    ("What is the historical importance of the city of Hyderabad?", "Hyderabad is a city in Sindh province, known for its cultural heritage, historical monuments, and role in the independence movement."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    ("What is the role of the Pakistan Broadcasting Corporation (PBC)?", "The PBC is responsible for public radio broadcasting in Pakistan, providing news, entertainment, and educational programs to the public."),
    ("What was the significance of the 2014 APS attack in Peshawar?", "The 2014 APS attack in Peshawar was a terrorist attack on a school, resulting in the deaths of over 140 people, mostly children, and leading to a major crackdown on terrorism."),
    ("What is the historical importance of the city of Sargodha?", "Sargodha is a city in Pakistan, known for its agricultural production, particularly citrus fruits, and its role in the independence movement."),
    ("What was the impact of the 1979 Iranian Revolution on Pakistan?", "The 1979 Iranian Revolution influenced Pakistan's Shia population and impacted regional geopolitics, leading to increased sectarian tensions."),
    ("What is the role of the Pakistan Civil Aviation Authority (PCAA)?", "The PCAA is responsible for regulating and overseeing civil aviation activities in Pakistan, ensuring safety, and managing airports."),
    ("What was the significance of the 1965 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1965 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Quetta?", "Quetta is the capital of Balochistan province, known for its strategic location, military presence, and role in regional geopolitics."),
    ("What was the impact of the 2014 military operation Zarb-e-Azb?", "Operation Zarb-e-Azb was a military operation launched by Pakistan against militant groups in North Waziristan, leading to significant security improvements."),
    ("What is the role of the Pakistan Rangers?", "The Pakistan Rangers are a paramilitary force responsible for maintaining law and order, particularly in border regions and urban areas."),
    ("What was the significance of the 2016 Quetta hospital bombing?", "The 2016 Quetta hospital bombing was a terrorist attack targeting a gathering of lawyers, resulting in significant casualties and highlighting issues of security."),
    ("What is the historical significance of the city of Multan?", "Multan is an ancient city in Pakistan, known for its Sufi shrines, historical monuments, and role in trade and commerce."),
    ("What was the impact of the 2008 economic crisis on Pakistan?", "The 2008 global economic crisis led to significant economic challenges for Pakistan, including inflation, energy shortages, and a balance of payments crisis."),
    ("What is the role of the Pakistan Coast Guards?", "The Pakistan Coast Guards are responsible for protecting Pakistan's maritime borders, combating smuggling, and ensuring coastal security."),
    ("What was the significance of the 1964 Rann of Kutch conflict?", "The Rann of Kutch conflict in 1964 was a territorial dispute between India and Pakistan over a salt marsh region, leading to military skirmishes and eventual arbitration."),
    ("What is the historical significance of the city of Sialkot?", "Sialkot is an industrial city in Pakistan, known for its production of sports goods, surgical instruments, and its role in the independence movement."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    ("What is the role of the Pakistan Air Force?", "The Pakistan Air Force is responsible for the aerial defense of Pakistan, playing a key role in national security and regional stability."),
    ("What was the significance of the 1990 Gulf War for Pakistan?", "During the 1990 Gulf War, Pakistan contributed troops to protect Saudi Arabia's holy sites and supported the US-led coalition."),
    ("What is the historical significance of the city of Karachi?", "Karachi is Pakistan's largest city and economic hub, known for its port, diverse population, and role in the independence movement."),
    ("What was the impact of the 2018 general elections in Pakistan?", "The 2018 general elections resulted in the victory of Imran Khan's PTI, marking a significant shift in Pakistan's political landscape."),
    ("What is the role of the Pakistan Frontier Corps?", "The Pakistan Frontier Corps are a paramilitary force responsible for border security, counterinsurgency, and maintaining law and order in the tribal areas."),
    ("What was the significance of the 2006 Balochistan conflict?", "The 2006 conflict in Balochistan involved clashes between Baloch nationalists and Pakistani security forces, highlighting issues of autonomy and resource distribution."),
    ("What is the historical importance of the city of Faisalabad?", "Faisalabad, formerly known as Lyallpur, is an industrial city in Pakistan, known for its textile industry and economic importance."),
    ("What was the impact of the 2011 Osama bin Laden operation on Pakistan?", "The 2011 operation by US forces to kill Osama bin Laden in Abbottabad, Pakistan, led to strained US-Pakistan relations and raised questions about Pakistan's sovereignty and intelligence capabilities."),
    ("What is the role of the Pakistan Maritime Security Agency (PMSA)?", "The PMSA is responsible for enforcing maritime law, protecting Pakistan's maritime interests, and conducting search and rescue operations."),
    ("What was the significance of the 1998 nuclear tests on Pakistan's international relations?", "The 1998 nuclear tests conducted by Pakistan established it as a nuclear-armed state, leading to international sanctions and significant changes in regional security dynamics."),
    ("What is the role of the Pakistan National Shipping Corporation (PNSC)?", "The PNSC is responsible for providing maritime transportation services, managing the national fleet, and playing a key role in Pakistan's trade and logistics."),
    ("What was the significance of the 1971 Bangladesh Liberation War?", "The 1971 Bangladesh Liberation War led to the secession of East Pakistan and the creation of the independent state of Bangladesh."),
    ("What is the historical importance of the city of Hyderabad?", "Hyderabad is a city in Sindh province, known for its cultural heritage, historical monuments, and role in the independence movement."),
    ("What was the impact of the 2013 general elections in Pakistan?", "The 2013 general elections marked the first democratic transfer of power in Pakistan's history, with Nawaz Sharif's PML-N winning a significant victory."),
    

    ]
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.executemany("INSERT INTO qa_pairs (question, answer) VALUES (?, ?)", predefined_data)
    conn.commit()
    conn.close()

# Call the function to insert predefined data
insert_predefined_data()

# Function to calculate the similarity between two strings
def calculate_similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# Fetch answer from the database with 70% similarity
def fetch_answer(question):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("SELECT question, answer FROM qa_pairs")
    results = c.fetchall()
    conn.close()
    
    best_match = None
    highest_similarity = 0
    
    for q, a in results:
        similarity = calculate_similarity(question, q)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = a
    
    if highest_similarity >= 0.7:
        return best_match
    else:
        return None

# Insert a new question-answer pair into the database
def insert_qa_pair(question, answer):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("INSERT INTO qa_pairs (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    answer = fetch_answer(question)
    
    if answer:
        return jsonify({"answer": answer})
    else:
        return jsonify({"answer": "I don't know the answer. Please provide the expected answer."})

@app.route('/learn', methods=['POST'])
def learn():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    
    if not question or not answer:
        return jsonify({"error": "Question and answer are required"}), 400
    
    insert_qa_pair(question, answer)
    return jsonify({"message": "Learned new question-answer pair"}), 201

if __name__ == '__main__':
    app.run(debug=True)
