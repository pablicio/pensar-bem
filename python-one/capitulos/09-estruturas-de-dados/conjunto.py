categorias = {"fruta", "legume", "fruta", "verdura"}
print(categorias)          # {'fruta', 'legume', 'verdura'}
print(len(categorias))     # 3

a = {"tomate", "alface"}
b = {"alface", "cenoura"}

print(a & b)   # {'alface'}      em ambos
print(a | b)   # união
print(a - b)   # só em a
