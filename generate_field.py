
# coder Koo Bonchan, LastEdit 17.11.14

# PROBLEM SPECIFICATION
# customer-dependent variable ==> weight
# requirement-dependent variable ==> cost
# customer-requirement dependent ==> value
# cost[0 to req-1], weight[0 to custo-1], val[0 to req-1][0 to custo-1] type int
# score[i] = sigma(j = custo) w[j] val[i][j]
# decision vector x[0 to req-1] type bool

# PRESET VALUE
# req, custo
# cost_min, cost_max
# weight_min, weight_max
# val_min, val_max
req = 25
custo = 20
costmin = 1
costmax = 5
weightmin = 1
weightmax = 5
valuemin = 0
valuemax = 9



class generate_field(): # generate NRP setup
    def __init__(self, req, custo):
        self.req = req
        self.custo = custo
        self.cost = [999999 for i in range(req)]
        self.weight = [0 for i in range(custo)]
        self.value = [[-1 for j in range(custo)] for i in range(req)]
        self.score = []


    def set_value(self, field, value, idx1, idx2 = -1):
        if field == "cost":
            self.cost[idx1] = value
        elif field == "weight":
            self.weight[idx1] = value
        elif field == "value":
            self.value[idx1][idx2] = value
        else:
            print("value_not_set")

    def eval_score(self):
        self.score = [0 for j in range(self.req)]
        for i in range(self.req):
            for j in range(self.custo):
                self.score[i] += self.weight[j] * self.value[i][j]

    def get_cost(self):
        return self.cost
    def get_weight(self):
        return self.weight
    def get_value(self):
        return self.value
    def get_score(self):
        return self.score