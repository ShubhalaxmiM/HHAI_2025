fewshot_decompose= """
Please tell me the necessary questions that need to be answered in order to verify the following claim. Take into account the speaker and the date of the claim, if necessary. Generate as many questions as you can think of:

Claim: Back when I was studying it, two out of three families that ended up in bankruptcy after a serious medical problem had health insurance.
Speaker: Elizabeth Warren
Date:October 15, 2019
>>>>>>
Followup Question: Is there any published research on the relationship bewtween medical debt and bankruptcy?
Followup Question: What do people cite as reasons for bankruptcy in bankruptcy applications?
Followup Question: When was Warren studying the issue of medical debt and bankruptcy?
Followup Question: Has something changed in health insurance policy between Warren's research period and when this claim was made?
Followup Question: How many families ended up in bankruptcy after a serious medical problem having health insurance?
------
Claim: Under my administration, 7 million Americans have come off of food stamps, and 10 million people have been lifted off of welfare.
Speaker: Donald Trump
Date: February 04, 2020
>>>>>>
Followup Question: What does "lifted off of welfare" concretely mean? 
Followup Question: Have these people taken off of such programs not because of their improved financial situation, but because of restrictions to the access to the program?
Followup Question: Is this improvement correlated to changes made by his administration, or is it part of a trend that was already there?
------
Claim: President Trump has sent 14,000 American troops to the (Middle East) region since May. So he can't tell his political rallies that he's getting troops out of endless wars when he's sending 14 times the amount back into the region.
Speaker: Brett McGurk
Date: October 20, 2019
>>>>>>
Followup Question: What does Pentagon say about recent troop deployment to the middle east region? 
Followup Question: From which countries did Trump remove troops?
Followup Question: Which countries did Trump deploy new troops to?
Followup Question: What is the most recent available data on troop distribution in countries in middle east?
Followup Question: How is sending more troops leading to a resolve in the middle east?
Followup Question: Does president Trump have other intentions with sending so many troops?
Followup Question: How many of these forces are occupying maritime space and not stationed on land in the middle east?
------
Claim: After pushing through a red flag law in the New Mexico Senate, Gov. Michelle Lujan Grisham ‚has had the firearms of her guards and household seized.
Speaker: Facebook post
Date: February 09, 2020
>>>>>>
Followup Question: What law regarding did Governor of new mexico support recently?
Followup Question: Were guns seized from the governor's home?
Followup Question: Were guns seized from the officers who protect the governor?
------
Claim: Says immigrants wanted by ICE have victimized ""tens of thousands of children"" in North Carolina.
Speaker: Dan Forest
Date: November 25, 2019
>>>>>>
Followup Question: What is the enforcement policy of illegal immigration in North Carolina?
Followup Question: Have undocumented immigrants victimized \"tens of thousands\" of children in North Carolina?
Followup Question: What is the statistics about violent crimes committed by illegal immigrants?
Followup Question: Are records kept regarning crimes committed by illegal immigrants?
Followup Question: Are records kept regarding the age of the victims of the violent crimes committed by illegal immigrants?
Followup Question: What are the common types of crimes committed by illegal immgrants?
------
Cliam: Pete Buttigieg is a favorite candidate of Wall Street and the health care industry.
Speaker: Bernie Sanders
Date: February 7, 2020
>>>>>>
Followup Question: What kind of support is Buttigieg supposedly receiving that could lead to him being 'a favourite candidate of Wall Street and health care industry'? Are there hard numbers to support that?
Followup Question: Did Pete Buttigieg receive a  formal political endorsement from related players in the industry?
Followup Question: Further investigation reveals that the numbers can look different based on what is considered the health care industry, so what does the Sanders campaign mean specifically when it refers to 'health care industry'?
Followup Question: Is there a way to further break down the data in terms of 'health care industry'?
Followup Question: How do the other candidates' fundraising compare on funding from various levels of the health care industry?
Followup Question: How do Sanders' own campaign contributions compare?Has he received any support from any facet of the health care industry?
Followup Question: What source did the Sanders campaign use to come with this claim? What specific campaign contribution trends does the Center for Responsive Politics track/report?
-----
Claim: {}
>>>>>>
"""

aggregate="""
Based on the evidence, decide if the claim is [TRUE] or [HALF-TRUE] or [FALSE]. First give the prediction, then a justification of the prediction using the evidence. Print in the structure demonstrated in the following examples. Do not repeat the example in the output.

A claim is [TRUE] if it is accurate and there's nothing significant missing or if the claim is accurate but needs clarification or additional information.
A claim is [HALF-TRUE] if it is partially accurate but leaves out important details or things taken out of context.
A claim is [FALSE] it is not accurate or if the statement contains an element of truth but ignores critical facts that would give a different impression.
-----
Claim: Back when I was studying it, two out of three families that ended up in bankruptcy after a serious medical problem had health insurance.
Speaker: Elizabeth Warren
Date:October 15, 2019

Evidence:
There is research around medical debt and bankruptcy but it is controversial. Elizabeth Warren herself published on the issue of debt and bankruptcy while she was in Harvard Law school.Scholars are also quick to note that, in the majority of so-called "medical bankruptcies" identified in the paper, the issue wasn't debts incurred to pay off health care bills. Rather, the bigger problem was foregone income because people couldn't work.
Warrent studied this issue when she was in Harvard Law school. Health insurance is more generous today than it was when Warren studied it, thanks to the Affordable Care Act. And insuring everyone - even as generously as Medicare For All suggests - wouldn't necessarily address the issue of foregone income when people are sick, which the research suggests is a bigger financial concern.

Prediction: [TRUE]

Justification:
Warren’s claim comes from a paper that is controversial, and whose methods and interpretation have been called into question. That said, this statistic is fairly specific, and her wording in the claim precise. In itself, it’s a fair reflection of what the paper says. Where caution is more important: Warren says this finding suggests the cost of health care is what’s causing Americans financial harm. That isn’t necessarily borne out, and requires more scrutiny. This statement is accurate but would benefit from more information. We rate it [TRUE].
------
Claim: Under my administration, 7 million Americans have come off of food stamps, and 10 million people have been lifted off of welfare.
Speaker: Donald Trump
Date: February 04, 2020

Evidence:
When Donald Trump says 'lifted off of welfare', he most likely means that people who needed welfare programs, no longer eed them because of improved financial situation. But the wway records are kept, 'lifted off' simply means a reduction in the number of people receiving the benefits of welfare prorammes. The Trump administration finalized a rule in late 2019 that tightens guidelines on who can receive benefits and for how long.The changes are expected to move more "able-bodied" adults into the workforce U.S. Agriculture Secretary Sonny Perdue said in a news release. The rule was projected to end benefits for about 700,000 people. SNAP, one of the welfare programs likely being referred to by Trump, participation was falling since before Trump took office, a trend that experts say is likely due to a growing economy.Participation in the program usually follows along with the official poverty rate, which has been falling since 2010.

Prediction: [HALF-TRUE]

Justification:
Trump said, "Under my administration, 7 million Americans have come off of food stamps, and 10 million people have been lifted off of welfare."
 Trump’s claim that 7 million Americans have come off food stamps since he took office isn’t too far off, although some discrepancies in reporting show slightly skewed data. The decline is also likely due to both the growing economy and the administration’s policy changes that have affected eligibility for some groups. 
 But his broad welfare claim overshoots actual caseloads and appears to include programs that provide benefits to children and seniors as well as working adults. 
 We rate this [HALF-TRUE].
------
Claim: President Trump has sent 14,000 American troops to the (Middle East) region since May. So he can't tell his political rallies that he's getting troops out of endless wars when he's sending 14 times the amount back into the region.
Speaker: Brett McGurk
Date: October 20, 2019

Evidence:
The Pentagon has said it will shift about 1,000 American troops from Syria to western Iraq.
From which countries did Trump remove troops? American troops McGurk said he got his numbers from the Pentagon, which touted its troop commitments in an Oct. 11 press release announcing the deployment of about 3,000 U.S. forces to Saudi Arabia.The press release said the Pentagon had "increased the number of forces by approximately 14,000 to the U.S. Central Command area of responsibility" since May. Experts on foreign policy say that, the largest numbers of U.S. forces currently stationed in or near the Middle East are likely in Bahrain, Iraq, Saudi Arabia, Kuwait, Qatar and Afghanistan. According to June data from the Pentagon - which omits numbers for countries with ongoing operations such as Syria, Iraq and Afghanistan - there were at that time 283 total U.S. forces in Egypt, 76 in Israel, 20 in Lebanon, 1,750 in Turkey, 84 in Jordan, 2,077 in Kuwait, 535 in Saudi Arabia, 19 in Yemen, 17 in Oman, 374 in the United Arab Emirates, 636 in Qatar, and 4,865 in Bahrain.Those numbers include active duty personnel, national guard and reserve personnel and civilian personnel.According to the Royal Institute of International Affairs , a London think tank, they do not include temporary forces or classified special forces operating in secret.The June numbers are also outdated.

Prediction: [TRUE]

Justification:
McGurk said, "President Trump has sent 14,000 American troops to the (Middle East) region since May. So he can't tell his political rallies that he's getting troops out of endless wars when he's sending 14 times the amount back into the region." His number matches what the Pentagon has publicly reported in press releases and briefings.
We rate this statement [TRUE].
------
Claim: After pushing through a red flag law in the New Mexico Senate, Gov. Michelle Lujan Grisham‚ has had the firearms of her guards and household seized.
Speaker: Facebook post
Date: February 09, 2020

Evidence:
This story was inspired by Lujan Grisham's support of the proposed Extreme Risk Firearm Protection Order Act that passed the state Senate on Feb. 7.It passed the House on Feb. 13.Lujan Grisham, who applauded its passage , is expected to sign the bill. The laws allow police to petition a court to order the temporary removal of firearms from a person who may be dangerous, or to block the person from obtaining a firearm.After a set amount of time, the firearm is either returned to the person or the court order is extended.There is no evidence that guns were seized from Lujan Grisham's home or from her security detail after passage of the law. The state police officers who protect her remain armed, the governor's spokesman Tripp Stelnicki told PolitiFact.

Prediction: [FALSE]

Justification:
There is no evidence that guns were seized from Lujan Grisham’s home or from her security detail after passage of the law. We rate this statement [FALSE].
------
Claim: Says immigrants wanted by ICE have victimized ""tens of thousands of children"" in North Carolina.
Speaker: Dan Forest
Date: November 25, 2019

Evidence:
After the 2018 election, a new wave of Democratic sheriffs vowed to halt their jails' practice of holding undocumented immigrants on behalf of U.S. Immigration and Customs Enforcement, known as ICE.The sheriffs' position: if a judge or magistrate grants a person's release, he or she should be released -- regardless of immigration status.In response, some Republicans said the sheriffs were endangering public safety, and the GOP-controlled North Carolina legislature passed a bill that would require sheriffs to comply with ICE requests.But Democratic Gov.Roy Cooper vetoed it. There is no federal government database or study tracking how many people have been victimized by undocumented immigrants or the age of the victims. ICE doesn't track crimes committed by immigrants in the United States illegally, nor does it track the age of victims of those crimes.North Carolina-specific data isn't available, either. Neither the NC Attorney General's Office, the State Bureau of Investigation, nor the Department of Public Safety tracks the statistic Forest mentioned, according to spokespeople for those agencies. A story by WBTV  details 1,020 criminal charges and 407 convictions for immigrants sought by ICE in 2019 but released from NC jails before ICE could obtain custody. But many of those charges were for driving offenses, larceny and other nonviolent crimes.

Prediction: [FALSE]

Justification:
In a speech about immigrants in the country illegally, Forest said "we have tens of thousands of children in our state that have been victims of these violent criminals already." There’s no available data to support his claim. We rate it [FALSE].
------
Cliam: Pete Buttigieg is a favorite candidate of Wall Street and the health care industry.
Speaker: Bernie Sanders
Date: February 7, 2020

Evidence:
Staffers used  data from the Center for Responsive Politics, a nonprofit group that operates the website OpenSecrets.org and tracks money from individuals and political action committees donated to political candidates and members of Congress. The center analyzes Federal Election Commission data and sorts contributions by categories based on the economic sector from which they come. The Sanders campaign used OpenSecrets data it obtained in December 2019. OpenSecrets defines its health sector by contributions from PACs and individuals working in various health industries.Based on this sweeping categorization, Sanders is ahead of Buttigieg in health sector donations. The Vermont senator received $2,910,894, while the former South Bend mayor trailed closely behind with $2,713,038. However, when you break down this data by industries within the health sector, Buttigieg comes out ahead of Sanders in contributions from pharmaceutical companies and also for health services/HMOs which includes groups like large insurance companies. But even this point is nuanced. Former Vice President Joe Biden has received the most money of any Democratic candidate from the pharmaceuticals and health products sector if contributions from his leadership political action committee are included. Leadership PACs are committees unaffiliated with campaigns that can still receive contributions and financially support candidates. In the health care industry categories of hospitals/nursing homes and health professionals, Sanders has received the most in dollar contributions. The Sanders campaign sent us a list of pharmaceutical and health insurance executives that have contributed to Buttigieg, including employees and executives from AbbVie, Aetna, Anthem, Eli Lilly and Co., Merck & Co. and Pfizer.The actual composition of donors in the health category can't be known without analyzing OpenSecrets' full data set- which we could not do since it's not publicly available. OpenSecrets does, however, analyze the percentage of small donor donations (less than $200) and large contributions for each presidential candidate. And 56% of Sanders' contributions are from small donors, while 45% of Buttigieg's campaign contributions come from that same group.  

Prediction: [HALF-TRUE]

Justification:
Sanders' use of the phrase "health care industry" in this instance is too broad to support the point he is trying to make.According to recently updated OpenSecrets data, Sanders has received more donations from the health sector than any other 2020 presidential candidate. However, when the broad "health sector" category is narrowed down to pharmaceutical and health insurance companies, which are two targets of Sanders' campaign, Buttigieg is shown to have received more donations than Sanders. He has also received donations from top pharmaceutical executives - offering evidence to support Sanders' claim. But in specifying donations from the pharmaceutical/health products sector, Biden tops Buttigieg when factoring in contributions to Biden's leadership PAC. Context is also important. It's likely a large number of Sanders' health care contributions are from nurses and doctors as individuals. There's no way to identify whether this support was related to the candidate's health policies or motivated by other reasons. Sanders' claim has some truth to it but is imprecise. For this reason, we rate the claim [HALF-TRUE].
-----
Claim: {}
""" 



direct_decompose="""
Please tell me the necessary questions that need to be answered in order to verify the following claim. Take into account the speaker and the date of the claim, if necessary. Generate as many questions as you can think of. Preface each question with 'Followup Question:'

Claim: {}
"""

llama_aggregate="""
Based on the evidence, decide if the claim is [TRUE] or [HALF-TRUE] or [FALSE]. First print the prediction, then justify the prediction using the evidence. The label in the prediction and justification must match. Print in the structure demonstrated in the following examples.

A claim is [TRUE] if it is accurate and there's nothing significant missing or if the claim is accurate but needs clarification or additional information.
A claim if [HALF-TRUE] if it is partially accurate but leaves out important details or things taken out of context.
A claim is [FALSE] it is not accurate or if the statement contains an element of truth but ignores critical facts that would give a different impression.
-----
Claim: {}
"""

keyword_extract = """You're a fact checking assistant. The following claim needs to fact checked. Tell me the keywords to find evidence to fact check this claim. Separate keywords with '/'.
{}
"""

