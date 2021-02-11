actorshow = [1, 2, 1, 3]
wantshow = []
# for actor in actors:
#     for show in actor.show_actor.all():
#         actorshow.append(show)
for i in range(len(actorshow)):
    for j in range(len(actorshow)):
        if i <= j:
            pass
        elif actorshow[i] == actorshow[j]:
            pass
        else:
            wantshow.append(actorshow[i])
print(wantshow)
