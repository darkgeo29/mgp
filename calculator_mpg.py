class mgp_object(object):
    def __init__(self, name, prod_init, prod_weight, lvup_price_init, lvup_price_weight,sectors):
        self.name = name
        self.level = 0
        self.prod_value = int(prod_init)
        self.prod_weight = float(prod_weight)

        self.lvup_price_value = int(lvup_price_init)
        self.lvup_price_weight = float(lvup_price_weight)

        self.need_sectors = sectors

        self.buying_time = "0"

    def level_up(self, n=1):
        self.level += n
        self.prod_value = round(self.prod_value * self.prod_weight)
        self.lvup_price_value = round(self.lvup_price_value * self.lvup_price_weight)


class calculator():
    def __init__(self):
        #실제 디비
        self.mgp_objs = []
        self.load_mgp_objects()
        # sectors
        self.sectors = {"들판":31906,"설산과초원":113000000,"해변":211000000000000000000,"바다":582000000000000000000000000000000000}
        #내가 가진거
        self.my_exist_objs = []
        self.my_exist_objs_names = []
        self.my_sectors_buying_time = {}
        self.money = 90


    def next_sec(self):
        pass

    def load_mgp_objects(self):
        obj_file = open('mgp/obj.txt', 'r', encoding='UTF8')
        lines = obj_file.readlines()
        for line in lines:
            line = line.rstrip()
            tokens = line.split('\t')
            name = tokens[0]
            id = int(tokens[1])
            prod_init = tokens[2]
            prod_weight = tokens[3]
            lvup_init = tokens[4]
            lvup_weight = tokens[5]
            sectors = []
            if id > 3:
                sectors.append("들판")
            if id > 7:
                sectors.append("설산과초원")
            if id > 12:
                sectors.append("해변")
            if id > 17:
                sectors.append("바다")
            obj = mgp_object(name,prod_init,prod_weight,lvup_init,lvup_weight,sectors)
            self.mgp_objs.append(obj)

    def buy_object(self, name):
        for obj in self.mgp_objs:
            check_obj = True
            for obj_sec in obj.need_sectors:
                if obj_sec not in self.my_sectors_buying_time:
                    check_obj = False
            if obj.name == name and check_obj:
                self.money -= obj.lvup_price_value
                obj.level += 1
                obj.lvup_price_value = round(obj.lvup_price_value * obj.lvup_price_weight)
                self.my_exist_objs.append(obj)
                self.my_exist_objs_names.append(name)

    def production_myobjs(self):
        production_values = 0
        for obj in self.my_exist_objs:
            self.money += obj.prod_value
            production_values += obj.prod_value
        return production_values

    def make_strategy(self):
        all_path_map = []
        max_lv = 5
        target_cnt = 5
        path_map = ""
        for obj in self.mgp_objs[:target_cnt]:
            pass

    def game_start(self, path, inverse_path):
        self.buy_object("세계수")
        sec = 0
        not_clear = True
        table = open(inverse_path, 'w', encoding='utf8')
        table.write("시간\t초당 생산량\t돈\t세계수\t사슴\t잔디\t벚꽃\t꽃밭\t래서판다\t양\t침엽수\t야생화 꽃밭\t순록\t사막여우\t자작나무 숲\t무지개\n")
        output = open(path, 'w', encoding='utf8')
        item_cnt = 0
        before_len = 1
        while(not_clear):
            sec += 1
            p_value = self.production_myobjs()
            # 싼거 사기
            for name, price in self.sectors.items():    #섹터 사기
                if name not in self.my_sectors_buying_time and price < self.money:
                    self.my_sectors_buying_time[name] = str(sec)
                    self.money -= price
            for obj in self.mgp_objs:       #새 obj 사기
                if obj.lvup_price_value < self.money and obj.name not in self.my_exist_objs_names:
                    self.buy_object(obj.name)
                    for my_obj in self.my_exist_objs:
                        if my_obj.name == obj.name:
                            my_obj.buying_time = str(sec)
            # Level up 찍기
            for obj in self.my_exist_objs:
                if obj.lvup_price_value < self.money:
                    self.money -= obj.lvup_price_value
                    obj.level_up()

            if len(self.my_exist_objs) > item_cnt:
                print("item buying "+str(sec)+"초")
                print(self.my_exist_objs[item_cnt].name)
                output.write("----- "+str(sec)+'초\n')
                for obj in self.my_exist_objs:
                    output.write(obj.name + '\t' + str(obj.level)+'\n')
                output.write("돈\t"+str(self.money)+'\n')
                output.write("초당 생산량\t"+str(p_value)+'\n')
                item_cnt = len(self.my_exist_objs)

            if "무지개" in self.my_exist_objs_names:
                not_clear = False
                for obj in self.my_exist_objs:
                    print(obj.name +'\t'+obj.buying_time)
                    output.write(obj.name +'\t'+obj.buying_time+'\n')
                for sec, time in self.my_sectors_buying_time.items():
                    output.write(sec + '\t' + time + '\n')
                output.write("돈\t" + str(self.money) + '\n')
                output.write("초당 생산량\t" + str(p_value) + '\n')


            if len(str(p_value)) > before_len:
                table.write(str(sec)+'\t'+str(p_value)+'\t'+str(self.money) )
                for obj in self.my_exist_objs:
                    table.write('\t'+str(obj.level))
                for i in range(0,13-len(self.my_exist_objs)):
                    table.write('\t0')
                table.write('\n')
                before_len = len(str(p_value))

        output.close()
        table.close()

    def marshmallow(self, path,seconds=60):
        self.buy_object("세계수")
        sec = 0
        not_clear = True

        output = open(path, 'w', encoding='utf8')
        item_cnt = 0
        while(not_clear):
            sec += 1
            p_value = self.production_myobjs()
            if self.money < self.mgp_objs[item_cnt].lvup_price_value and self.money + (p_value*seconds) > self.mgp_objs[item_cnt].lvup_price_value:
                continue
            # 싼거 사기
            for name, price in self.sectors.items():    #섹터 사기
                if name not in self.my_sectors_buying_time and price < self.money:
                    self.my_sectors_buying_time[name] = str(sec)
                    self.money -= price
            for obj in self.mgp_objs:       #새 obj 사기
                if obj.lvup_price_value < self.money and obj.name not in self.my_exist_objs_names:
                    self.buy_object(obj.name)
                    for my_obj in self.my_exist_objs:
                        if my_obj.name == obj.name:
                            my_obj.buying_time = str(sec)
            # Level up 찍기
            for obj in self.my_exist_objs:
                if obj.lvup_price_value < self.money:
                    self.money -= obj.lvup_price_value
                    obj.level_up()

            if len(self.my_exist_objs) > item_cnt:
                print("item buying "+str(sec)+"초")
                print(self.my_exist_objs[item_cnt].name)
                output.write("----- "+str(sec)+'초\n')
                for obj in self.my_exist_objs:
                    output.write(obj.name + '\t' + str(obj.level)+'\n')
                output.write("돈\t" + str(self.money) + '\n')
                output.write("초당 생산량\t" + str(p_value) + '\n')
                item_cnt = len(self.my_exist_objs)

            if "무지개" in self.my_exist_objs_names:
                not_clear = False
                for obj in self.my_exist_objs:
                    print(obj.name +'\t'+obj.buying_time)
                    output.write(obj.name +'\t'+obj.buying_time+'\n')
                for sec, time in self.my_sectors_buying_time.items():
                    output.write(sec + '\t' + time + '\n')
                output.write("돈\t" + str(self.money) + '\n')
                output.write("초당 생산량\t" + str(p_value) + '\n')


        output.close()






def main():
    simulator = calculator()
    #simulator.game_start("mgp/logs.txt", "mgp/inverse_cal.txt")
    #simulator.marshmallow("mgp/marshmallow_logs.txt.", 60)

    for i in range(1,11):
        simulator = calculator()
        sec = i*60
        simulator.marshmallow("mgp/marshmallow_logs.txt."+str(sec), sec)


if __name__ == "__main__":
  main()
