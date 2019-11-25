import re

dataFile = open('text_for_regular_expression_test.txt', mode='r', encoding='utf-8')
content = dataFile.read()
emails = re.findall(r'[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+', content)
mobiles = re.findall(r'\d{3}-\d{8}|1\d{10}', content)
urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)


print(emails)
print(mobiles)
print(urls)
# resFile = open('result.txt', mode='w', encoding='utf-8')
# resFile.write('emails:\n')
# resFile.write(str(emails))
# resFile.write('\nmobiles:\n')
# resFile.write(str(mobiles))
# resFile.write('\nurls:\n')
# resFile.write(str(urls))
# resFile.close()

dataFile.close()
