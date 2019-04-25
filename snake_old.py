# import pygame, random
#
# pygame.init()
# screen = pygame.display.set_mode([440,440])
# leave = False
#
#
# clock = pygame.time.Clock()
#
# class Head():
#     def __init__(self):
#         self.location = [random.randint(4,10) * 20,random.randint(4,10) * 20]
#         self.directions = ["up","right","down", "left"]
#         self.direction = random.randint(0,3)
#         return
#
#
#     def move(self):
#         turned = False
#         for event in pygame.event.get():
#             if event == pygame.QUIT: leave = True
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_q:
#                     leave == True
#                 elif event.key == pygame.K_UP and self.direction != 2 and not turned:
#                     self.direction = 0
#                     turned = True
#                 elif event.key == pygame.K_DOWN and self.direction != 0 and not turned:
#                     self.direction = 2
#                     turned = True
#                 elif event.key == pygame.K_RIGHT and self.direction != 3 and not turned:
#                     self.direction = 1
#                     turned = True
#                 elif event.key == pygame.K_LEFT and self.direction != 1 and not turned:
#                      self.direction = 3
#                      turned = True
#         if self.direction == 0:
#             self.location[1] -= 20
#         if self.direction == 1:
#             self.location[0] += 20
#         if self.direction == 2:
#             self.location[1] += 20
#         if self.direction == 3:
#             self.location[0] -= 20
#
#         if head.location[0] < 0:
#             head.location[0] = 420
#         if head.location[0] > 420:
#             head.location[0] = 0
#         if head.location[1] < 0:
#             head.location[1] = 420
#         if head.location[1] > 420:
#             head.location[1] = 0
#
#         return
#
# bodies = []
# head = Head()
# turns = 0
# food_spot = [random.randint(1, 20) * 20,random.randint(1, 20) * 20]
# while not leave:
#     clock.tick(15)
#     turns += 1
#     food = False
#     if head.location == food_spot:
#         food = True
#         food_spot = [random.randint(1, 20) * 20,random.randint(1, 20) * 20]
#     if (turns < 3):
#         food = True
#     if not food:
#         del bodies[0]
#     bodies.append([head.location[0],head.location[1]])
#     head.move()
#
#     screen.fill([255,255,255])
#
#     for part in bodies:
#         pygame.draw.rect(screen,[0,0,0],[part[0],part[1],20,20],0)
#         if part != bodies[0] and [part[0],part[1]] == head.location:
#             leave = True
#
#     pygame.draw.rect(screen,[0,0,0],[head.location[0],head.location[1],20,20],0)
#     pygame.draw.rect(screen,[255,0,0],[food_spot[0],food_spot[1],20,20],0)
#     pygame.display.flip()
# font = pygame.font.Font(None,20)
# score_text = font.render("Congrats you got " + str(len(bodies) - 2) + " before you failed epicly",1,(random.randint(0,250),random.randint(0,250),random.randint(0,250)))
# screen.blit(score_text,[10,200])
# pygame.display.flip()
# #raw_input()
# pygame.quit()