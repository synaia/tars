
import random

basic_form = [
    "Almost there to land your job!\nNow, please proceed to the assessment below ⤵️",
    "Just a few steps to your job! 🙌🏼\nYour next step is to fill in the assessment below ⤵️",
    "You're so close to your job!\nThe next task is to tackle the assessment below ⤵️",
    "Your job is just steps away!\nUp next is the assessment, please fill it out below ⤵️",
    "Nearly there! Job is within reach!\nThe next thing to do is fill out the assessment below ⤵️",
    "Steps away from your new job!\nNow, let's move on to the assessment below ⤵️",
    "Job ahead! Just a few steps!\nNext, please complete the assessment below ⤵️",
    "Your job is right around the corner!\nThe following step is to fill out the assessment below ⤵️",
    "Almost at the finish line!\nPlease proceed by filling out the assessment below ⤵️",
    "Just steps from your job!\nNow, kindly complete the assessment below ⤵️"
]

assesment_form = [
    "You've made great progress—well done! 🚀 Next, read the text aloud and send it as a voice note:",
    "You've advanced significantly—congratulations! 🚀 Please read the text aloud and submit it as a voice note:",
    "You've taken a big step forward—kudos! 🚀 In the next step, read the text aloud and send it:",
    "You've made an important leap—awesome job! 🚀 Read the text aloud and send it as a voice note, please:",
    "You've moved ahead impressively—great job! 🚀 Next step: read the text aloud and send it as voice note:",
    "You've achieved a major milestone—congrats! 🚀 Read the following text aloud and send it as a voice message:",
    "You've made remarkable progress—congratulations! 🚀 For the next step, read the text aloud and send it:",
    "You've taken a crucial step forward—nice work! 🚀 Please read aloud the text and send it as a voice note:",
    "You've made significant strides—well done! 🚀 Next, read the following text aloud and send a voice note:",
    "You've moved forward significantly—excellent! 🚀 In the next step, read aloud and send the text as voice note:"
]

assesment_form_text_1 = [
    "The resurgence of vinyl records has sparked a debate about the nostalgic appeal of analogue music versus the convenience of digital streaming. While some argue that vinyl's tactile experience enhances musical appreciation, others contend that streaming services provide unparalleled accessibility to diverse genres and artists.",
    "As millennials navigate the gig economy,they must confront the blurred lines between personal and professional brands. Social media influencers, in particular, face the daunting task of maintaining authenticity while monetizing their online presence. Can they escape the stigma of 'selling out' and preserve their artistic integrity?",
    "According to recent studies, millennials prioritize experiential travel, seeking cultural immersion and Instagram-worthy moments over material possessions. This shift in consumer behavior has significant implications for the hospitality industry, as hotels and resorts adapt to cater to the preferences of this tech-savvy demographic.",
    "The concept of micro-influencers has revolutionized the digital marketing landscape. With their niche audiences and high engagement rates, they're becoming increasingly attractive to brands seeking authenticity and precision targeting. As social media algorithms continue to evolve, it's crucial for marketers to adapt and harness the power of these online personalities.",
]


voice_note_1 = [
    "We got your voice note! ✅ You've made excellent progress—great job! 🚀 Last task: record a voice note (over 1 minute) responding to this open-ended question:",
    "Your voice note has arrived! ✅  You've done fantastic work—congratulations! 🚀 Final requirement: submit a voice note (minimum 1 minute) addressing the following query:",
    "Voice note received! ✅ You've achieved great progress—well done! 🚀 Complete the process by sending a voice note (at least 1 minute) answering the following:",
    "We've got your voice note! ✅  You've advanced impressively—awesome job! 🚀 The last step is to record and send a voice note (1+ minute) on the following topic:",
    "Your voice note has been successfully received! ✅  You've made amazing progress—congrats! 🚀 To finish, please provide a voice note (exceeding 1 minute) responding to the following question:",
    "Voice note received successfully! ✅ You've reached a significant milestone—brilliant work! 🚀 The final hurdle: recording a voice note (over 1 minute) to address the following inquiry:",
    "We've received your voice note! ✅  You've progressed wonderfully—great job! 🚀 Complete your awesome journey by submitting a voice note (longer than 1 minute) on the following theme:",
    "Your voice note is in! ✅ You've moved forward tremendously—excellent work! 🚀 The concluding, send a voice note (minimum 1 minute) exploring the following open-ended question:",
    "Voice note has been received! ✅  You've accomplished great strides—well done! 🚀 To conclude, please record and submit a voice note (at least 1 minute) on the following subject:",
    "Got your voice note! ✅  You've made substantial progress—fantastic job! 🚀 The last task involves recording a voice note (1+ minute) that thoughtfully addresses the following prompt:"
]

open_question_1 = [
    "If you could create a dream community or city from scratch, what would it look like, and what features would you include to make it the perfect place to live, work, and play?",
    "If you could switch lives with someone for a day, who would it be and why? What would you do during that day, and what do you think you would learn from the experience?",
    "What do you think are the most important qualities and skills that a person should have to be successful in their career, and how do you think you can develop those qualities and skills?",
    "Imagine you've been given a magical power to change one thing about your daily life for a year. What would it be and how would you use it?",
    "If you could plan the perfect weekend getaway with unlimited resources, where would you go and what would you do? What would make this trip so special and unforgettable?"
]

voice_note_2 = [
  "🎉 Your voice note has landed! Well done on completing all the steps, thanks! 😊",
  "👍 Your voice note arrived safely! Awesome job on finishing all tasks, thank you! 🙏",
  "📝 Your voice note received! Excellent work on completing every step, thanks a lot! 👏",
  "💬 Your voice note has dropped! Fantastic job on finishing all steps, appreciate it! 😊",
  "🎯 Your voice note is here! Great work on checking all the boxes, thank you! 👍",
  "📱 Your voice note arrived! You aced it by completing all steps, thanks so much! 🙏",
  "👂 Your voice note landed safely! Superb job on completing all tasks, thank you! 😊",
  "📝 Your voice note has been received! Outstanding work on finishing all steps, kudos! 👏",
  "🎉 Your voice note is in! Brilliant job on completing every step, thanks a ton! 😊",
  "💬 Your voice note has been delivered! Exceptional work on finishing all tasks, thanks! 🙏"
]

voice_note_received_yet = [
    "We've received your voice note and it's now under validation! 🎧",
    "Your voice note has arrived and is being verified! 🎧",
    "Your voice note is in and currently going through validation! 🎧",
    "We've got your voice note and it's being checked! 🎧",
    "Your voice note has been received and is now under review! 🎧"
]


switch_to_text = [
    "Kindly use text communication for now. Thanks! 💬",
    "Please shift to text communication for the moment. Much appreciated! 💬",
    "Switch to text messages for the time being, please. Thanks a lot! 💬",
    "For now, please use text to communicate. Appreciate it! 💬",
    "We'd appreciate it if you could use text communication for now. Thanks! 💬",
    "Please communicate via text for the time being. Thanks! 💬",
    "Text communication is preferred for now. Thank you! 💬",
    "Could you please switch to text communication for the time being? Thanks! 💬",
    "For the moment, please switch to text messages. Appreciate it! 💬",
    "Please use text communication temporarily. Thank you! 💬"
]


assignment_reminder = [
    "Remember to fill out the form - it's quick and easy! ⏱️",
    "Take a brief moment to complete the form, it's just a minute or two! 📝",
    "Don't miss this step! Fill out the form now, it's fast and simple 😊",
    "Complete the form in just a flash - it only takes 1-2 minutes ⏱️",
    "A minute or two is all it takes - fill out the form now! 📝",
    "Don't forget this important step: complete the form today! 📝",
    "Spend a minute or two to fill out the form - it's easy peasy! 😊",
    "Take a short break to complete the form - it's quick and painless! ⏱️",
    "Fill out the form in no time - it's a breeze! ⏱️",
    "Complete the form now and be done in just a minute or two! 📝"
]


friendly_reminder = [
    "Don't forget to wrap up the evaluation ⏰—you're almost there! 💼",
    "A gentle nudge to finish the assessment 🌈—your dream job awaits! 🎉",
    "Remember to finalize the evaluation checklist 📝—hiring is just around the corner! 👍",
    "Complete the evaluation and take one giant leap towards your new role 🚀!",
    "Hey, don't miss this step! Finish the evaluation to land your ideal job 💻",
    "A heads up to tie up the evaluation loose ends 🎀—you're almost hired! 😊",
    "Get ready to celebrate! Finish the evaluation to move forward with your hiring 🎉",
    "Take the final step towards your new adventure: complete the evaluation today 🌟!",
    "Wrap up the evaluation and get one step closer to joining our team 👫!",
    "Finish strong! Complete the evaluation to seal the deal on your new job 📈",
    "Your new career is within reach! Don't forget to finish the evaluation 🌱"
]

voice_note_reminder_1 = [
    "A quick reminder: speak the text and share it as a voice memo 🗣️",
    "Remember to read the text aloud and send it as audio 📢",
    "Read the text aloud and send it as a voice message 🎧",
    "Don't forget to voice the text and send it as a note 🎤",
    "Speak the text clearly and share it as a voice note 🎙️",
    "Kindly read the text aloud and record a voice message 🎤",
    "Please verbalize the text and send it as an audio note 📢",
    "A gentle reminder to read the text and send a voice memo 🎧",
    "Say the text aloud and send it as a voice recording 🗣️",
]

voice_note_reminder_2 = [
    "Be sure to complete the process: speak your answer and send a voice note 🎤.",
    "Remember the last step: respond out loud and send it as an audio message 🔊.",
    "Finish strong! Say your answer aloud and send a voice note 🎧.",
    "Final step: voice your answer and send it over as a voice message 📢.",
    "Don't forget: answer out loud and share it as a voice note 🎙️.",
    "Complete the task: speak your answer and deliver it via voice note 🎤.",
    "Make sure to answer aloud and send it as a voice recording 🗣️.",
    "Wrap it up: say your answer and send it as a voice note 🎧.",
    "Don't skip this: answer aloud and send an audio message 📣.",
    "Last step: respond verbally and send it as a voice note 🎙️.",
]



def random_message(m_list: list):
    l = len(m_list) - 1
    r = random.randint(0, l)
    return m_list[r]
