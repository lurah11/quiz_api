from rest_framework import serializers
from .models import Question, QuizInstance, Choices, Lesson
from django.contrib.auth import authenticate

class QASerializer(serializers.Serializer): # QA = Question and Answer Field 
    username = serializers.CharField()
    password = serializers.CharField()
    lesson_id = serializers.IntegerField()
    question_id= serializers.ListField(child=serializers.IntegerField())
    answer_id = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField(allow_null=True,required=False,default=None)))

    def validate(self,data): 
        validated_data = {}
        score = 0 
        no_of_correct = 0 
        user = authenticate(username=data['username'],password=data['password'])
        
        if not user : 
            raise serializers.ValidationError("Invalid username and or password")
        else :  
                validated_data['user'] = user.id
                try : 
                    lesson = Lesson.objects.get(id=data['lesson_id'])
                except : 
                    raise serializers.ValidationError("Wrong lesson ID")
                
                print("agustinus")
                validated_data['lesson'] = lesson.id
          
                question_qs = Question.objects.filter(lesson=lesson) #qs = Queryset 
       
                number_of_question = question_qs.count()

                answers = data['answer_id']

                if len(answers) > number_of_question:
                    raise serializers.ValidationError("Invalid number of answers, too many answer instance")
                if len(answers) < number_of_question: 
                    diff = number_of_question-len(answers)
                    for i in range(diff): 
                        answers.append(None)
                              
                for q_id,a_ids in zip(data['question_id'],answers): 
                        correct_answer = True 
                        try : 
                            question = Question.objects.get(id=q_id,lesson=lesson)
                        except:
                            raise serializers.ValidationError("Invalid Question ID, please check your ID and make sure it is exists!")
                        if not a_ids: 
                            correct_answer = False
                            continue
                        else : 
                            true_answers = Choices.objects.filter(question=question,is_true=True)
                            no_of_true_answers= true_answers.count()
                            if len(a_ids) != no_of_true_answers :
                                correct_answer = False
                            else:                                    
                                for a_id in a_ids : 
                                    try:
                                        answer = Choices.objects.get(id=a_id,question=question)
                                    except:
                                        raise serializers.ValidationError("Invalid Answer ID,, make sure the ID(s) are corresponding to the relevant question")
                                    if not answer.is_true:
                                        correct_answer = False
                                        break 
                        if correct_answer:
                            no_of_correct += 1
                                        
                           
        score = (no_of_correct/number_of_question) * 100 
        validated_data['score'] = score
                    
            

        return validated_data    
        




