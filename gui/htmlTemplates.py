css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 30%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
div.stButton > button:first-child {
                    background-color: #FAECE2;
                    color:#141314;
                    border-radius: 15px;
                }
div.stButton > button:hover {
                    background-color: #F9D6B1;
                    color:##8C8060;
                    border-radius: 15px;
                    }
download_button {
    display: inline-block;
    padding: 0.5em 1em;
    margin: 0.5em 0;
    font-size: 1em;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
    color: #FFF;
    background-color: #007bff;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s;
}
download_button:hover {
    background-color: #0056b3;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img.lovepik.com/original_origin_pic/18/12/19/b077a142c490cdf82a4aa9bd78f2d01a.png_wh860.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.lovepik.com/free-png/20211107/lovepik-student-png-image_400487470_wh1200.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

question_templete = ''' 


'''

