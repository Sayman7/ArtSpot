
class HomeChatroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Chatroom(models.Model):
    name = models.CharField(max_length=5000)
    
    def _str_(self):
        return self.name

class Chat(models.Model):
    chat_content = models.CharField(max_length=5000)
    user = models.CharField(max_length=5000)
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    


