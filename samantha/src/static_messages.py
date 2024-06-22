
import random

basic_form = [
    "Thanks for filling out the basic form 🙌🏼 Now, please proceed to the assessment below ⤵️",
    "We appreciate you completing the basic form 🙌🏼 Your next step is to fill in the assessment below ⤵️",
    "Grateful for your completion of the basic form 🙌🏼 The next task is to tackle the assessment below ⤵️",
    "Thank you for finishing the basic form 🙌🏼 Up next is the assessment, please fill it out below ⤵️",
    "Thanks for completing the basic form 🙌🏼 The next thing to do is fill out the assessment below ⤵️",
    "We thank you for filling in the basic form 🙌🏼 Now, let's move on to the assessment below ⤵️",
    "Your completion of the basic form is appreciated 🙌🏼 Next, please complete the assessment below ⤵️",
    "Thank you for submitting the basic form 🙌🏼 The following step is to fill out the assessment below ⤵️",
    "Cheers for finishing the basic form 🙌🏼 Please proceed by filling out the assessment below ⤵️",
    "We appreciate you finishing the basic form 🙌🏼 Now, kindly complete the assessment below ⤵️"
]

assesment_form = [
    "Hey, many thanks! You've made great progress—well done! 🚀 The last step is to send me a voice note 🗣️ of up to 2 minutes for evaluation.",
    "Thank you so much! You've advanced significantly—congratulations! 🚀 The final task is to submit a voice note 🗣️ that's no longer than 2 minutes for review.",
    "Appreciate it! You've taken a big step forward—kudos! 🚀 Now, just send me a voice note 🗣️ under 2 minutes for evaluation.",
    "Thanks a lot! You've made an important leap—awesome job! 🚀 The last part is to send a voice note 🗣️ of no more than 2 minutes for assessment.",
    "Thank you very much! You've moved ahead impressively—great job! 🚀 The concluding step is to record and send a voice note 🗣️ under 2 minutes for evaluation.",
    "Hey, thanks a ton! You've achieved a major milestone—congrats! 🚀 The final thing is to send over a voice note 🗣️ up to 2 minutes long for evaluation purposes.",
    "Much appreciated! You've made remarkable progress—congratulations! 🚀 Please send a voice note 🗣️ lasting no longer than 2 minutes for the final review.",
    "Thanks a bunch! You've taken a crucial step forward—nice work! 🚀 The last action is to submit a voice note 🗣️ of 2 minutes or less for evaluation.",
    "Thank you immensely! You've made significant strides—well done! 🚀 The final requirement is to send me a voice note 🗣️ that’s no longer than 2 minutes for assessment.",
    "Hey, big thanks! You've moved forward significantly—excellent! 🚀 The last step is to record a voice note 🗣️ of up to 2 minutes for evaluation purposes."
]


voice_note = [
    "We got your voice note! ✅ Thanks so much! You've made excellent progress—great job! 🚀 The process is now complete.",
    "Your voice note has arrived! ✅ Many thanks! You've done fantastic work—congratulations! 🚀 We've successfully finished the process.",
    "Voice note received! ✅ Thank you very much! You've achieved great progress—well done! 🚀 The process is now finalized.",
    "We've got your voice note! ✅ Thanks a ton! You've advanced impressively—awesome job! 🚀 The process is now complete.",
    "Your voice note has been successfully received! ✅ Thanks a bunch! You've made amazing progress—congrats! 🚀 The process is now finished.",
    "Voice note received successfully! ✅ Thank you so much! You've reached a significant milestone—brilliant work! 🚀 The process is complete.",
    "We've received your voice note! ✅ Many thanks! You've progressed wonderfully—great job! 🚀 The process is now concluded.",
    "Your voice note is in! ✅ Thanks a lot! You've moved forward tremendously—excellent work! 🚀 The process is now done.",
    "Voice note has been received! ✅ Big thanks! You've accomplished great strides—well done! 🚀 We've completed the process successfully.",
    "Got your voice note! ✅ Thank you immensely! You've made substantial progress—fantastic job! 🚀 The process is now wrapped up."
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

voice_note_reminder = [
    "a final reminder: don't skip the voice note! ⏰ it should only take 2 minutes. thanks! 😊",
    "almost there! just one more thing: record a quick 2-minute voice note, please. 👍",
    "don't miss the last step: leave a voice note (it's short, we promise!) 📝",
    "remember to add your voice note - it's the final hurdle! 🏁 (max 2 minutes, thanks) 👊",
    "last but not least, please record a voice note - just 2 minutes, we appreciate it! 😊",
    "a friendly reminder: voice notes are essential! please add yours (takes just 2 minutes). 📞",
    "you're nearly done! just add a brief voice note (under 2 minutes) and you're all set. 👌",
    "don't forget to leave a voice message - it's the last step, and it's quick! ⏱️",
    "almost finished! please take 2 minutes to record a voice note - thanks for your time! 🙏",
    "final check: have you added your voice note? it's a quick 2-minute task, we promise! 💯"
]


def random_message(m_list: list):
    l = len(m_list) - 1
    r = random.randint(0, l)
    return m_list[r]
