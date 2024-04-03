while(rcount<content_length):
        word_sum = user_prompt[lcount:rcount]
        response = client.chat.completions.create(
            model="chatEngine",
            messages=[
                {"role":"system","content":"You are an ai assistant designed to help people"},
                {"role":"user","content":"I am providing you with a content in english \n"
                                          "generate a summary of this content \n"
                                         + word_sum}
            ],
            temperature=0.7
        )
        summary = summary + response.choices[0].message.content
        lcount=lcount+100
        rcount=rcount+100
        
    final_response=client.chat.completions.create(
        model="chatEngine",
        messages=[
            {"role":"system","content":"You are an ai assistant designed to help people"},
            {"role":"user","content":"Provide me with a summary of the following text that I am providing you with \n"
                                     + summary}
        ],
        temperature=0.7
    )
    
    final_summary = final_response.choices[0].message.content
    
    print(final_summary)
