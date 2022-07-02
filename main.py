#Задание 1
#-----------------------------------
def set_cookbook(file):
  recipes = open(file)
  allfood = recipes.read()
#сначала разделим разные блюда меж собой:
  allfood = allfood.split('\n\n')
#но надо еще отделить друг от друга название, количество ингридиентов и ингридиенты, поэтому:
  allfood_newlist = []
  for i in allfood:
    allfood_newlist.append(i.split('\n'))
#теперь для удобства сделаем три списка - название блюда, кол-во ингридиентов и ингридиенты
  foodname_list = [j[0] for j in allfood_newlist]
  quantity_list = [k[1] for k in allfood_newlist]
  ingredient_list = [l[2:] for l in allfood_newlist]
#-----------------------------------
#сделаем разделение в списке ингридиентов на название, количество и меру, а потом создадим словари во вложенных списках
  m = 0
  while m < len(ingredient_list):
    n = 0
    while n < len(ingredient_list[m]):
      ingredient_list[m][n] = ingredient_list[m][n].split(' | ')
      #преобразуем вложенные списки в словари
      ingredient_list[m][n] = {key: value for key, value in zip(['ingredient_name', 'quantity', 'measure'], ingredient_list[m][n])}
      #не забудем сделать численный тип данных для количества ингридиента
      ingredient_list[m][n]['quantity'] = int(ingredient_list[m][n]['quantity'])
      n += 1
    m += 1
#-----------------------------------
#теперь можно закрыть файл
  recipes.close()
  return({food: ingredients for food, ingredients in zip(foodname_list, ingredient_list)})
cook_book = set_cookbook('recipes.txt')
#посмотрим, что получилось:
print(cook_book)
#-----------------------------------
#-----------------------------------
#Задание 2
def get_shop_list_by_dishes(dishes, person_count):
  pre_list = []
  for i in dishes:
    j = 0
    while j < len(cook_book[i]):
      pre_list.append(cook_book[i][j])
      j += 1
#теперь сделаем два списка - ингридиент и количество/мера для будущего словаря
  names_list = []
  k = 0
  while k < len(pre_list):
    names_list.append(pre_list[k]['ingredient_name'])
    del pre_list[k]['ingredient_name']
    k += 1
  final_dict = {}
  m = 0
  while m < len(names_list):
    if names_list[m] not in final_dict:
        #ингридиенты, встречающиеся единожды:
      if names_list.count(names_list[m]) == 1:
        final_dict[names_list[m]] = pre_list[m]
        m += 1
        #не единожды:
      else:
        n = 1
        lastindex = -1
        indicies = []
        summar_dict = {'measure': '', 'quantity': 0}
        #найдем словари, относящиеся к этому блюду, и будем суммировать параметр quantity:
        while n <= names_list.count(names_list[m]):
          indicies.append(names_list.index(names_list[m], lastindex + 1, len(names_list)))
          lastindex = names_list.index(names_list[m], lastindex + 1, len(names_list))
          n += 1
        summar_dict['measure'] = pre_list[m]['measure']
        for r in indicies:
          summar_dict['quantity'] += pre_list[r]['quantity']
        final_dict[names_list[m]] = summar_dict
        m += 1
    #если ингридиент встречается не единожды, но уже обработан, то пропускаем:
    else:
      m += 1
  #умножим теперь на количество персон:
  for t in final_dict:
    final_dict[t]['quantity'] *= person_count
  return(final_dict)
print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
#Задание 3
def merge_files(list_files):
  #сначала посчитаем количество строк в файлах:
  count_strings = {}
  for i in list_files:
    file = open(i)
    count_strings[i] = len(file.readlines())
    file.close()
  #новый список файлов, отсортированный по числу строк:
  newlist = sorted(count_strings, key=count_strings.get)
  #------------------------------------------
  res_file = open('result.txt', 'w')
  j = 0
  while j < len(newlist):
    res_file.write(newlist[j] + '\n')
    res_file.write(str(count_strings[newlist[j]]) + '\n')
    #открываем файл, чтобы взять из него список всех строк
    file = open(newlist[j])
    res_file.writelines(file.readlines())
    file.close()
    j += 1
    if j != len(newlist):
    #потому и цикл именно while, чтобы избавиться от лишнего переноса строки в конце:
      res_file.write('\n')
#посмотрим, что получилось:
merge_files(['1.txt', '2.txt', '3.txt'])