from random import choice
import random
import numpy as np
import copy
from collections import Counter


def evol(salary,k,costWeight,durationWeight,required_efforts,requiredE,eSkil,reqSk,task,employee,TPG,normalize,NUM_ELITE,POPULATION_SIZE,TOURNAMENT_SIZE,MUTATION_RATE):
    
    try:
       #get current level of task
        def get_precedence():
            ds=[0]*task
            dpac=[]
            for i in range(len(TPG)):
                dpac.append(TPG[i][1])
            
            c=dict(Counter(dpac))
            for i in range(task):
                if i not in dpac:
                    ds[i]=0
                else:
                    ds[i]=c[i]
            return ds

        #get task dependencies
        def get_dependence(tk):
            ds=[0]*task
            dpac=[]
            for i in range(len(TPG)):
                dpac.append(TPG[i][0])
            
            c=dict(Counter(dpac))
            
            for i in range(task):
                if i not in dpac:
                    ds[i]=0
                else:
                    ds[i]=c[i]
            return ds[tk]

        #depenced
        def taskDepPos(tk):
            dictt = {}
            for x, y in TPG:
                dictt.setdefault(x, []).append(y)
            

            return dictt[tk]

        #gantt chart precedence
        def preced(t):
            dictt = {}
            for x, y in TPG:
                dictt.setdefault(y, []).append(x)
            for i in range(task):
                if i not in dictt.keys():
                    dictt[i]=[]

            return dictt[t]

        #get employee salary
        def get_salary(e):
            for i in range(len(salary)):
                sal=salary[e]
            return sal

        #employee task dedication
        def getEmployeeTaskded(e,t,phe):
            new_p=phe.copy()
            dedication=new_p[e][t]
            return dedication

        #independent tasks
        def indepTask(curIndegree):
            currentTask=[]
            for i in range(len(curIndegree)):
                if(curIndegree[i]==0):
                    currentTask.append(i)
            return currentTask

        #employee current dedication
        def getDedicationEmployee(e,currentTask,phe):
            total=0
            for i in range(len(currentTask)):
                task=currentTask[i]
                total = total + getEmployeeTaskded(e,task,phe)
            return total

        #duration to finish the first task
        def durtoFinishFirst(currentTask, taskTol, reqEff):
            task_lenght=currentTask[0]
            tasks=[]
            tasks.append(task_lenght)
            

            effort=0

            if(taskTol[task_lenght] >0):
                effort=reqEff[task_lenght]/taskTol[task_lenght]
                #print('tasktol using first:: ',taskTol[task_lenght] )
            else:
                effort=1.78e+308
            #print("effort 1st",effort)
            for i in range(1, len(currentTask)):
                task = currentTask[i]
                efforts=0
                if(taskTol[task]>0):
                    efforts=reqEff[task]/taskTol[task]
                # print('tasktol using all:: ',taskTol[task] )
                else:
                    efforts=1.78e+308
            # print('effort all task',i, ' ',efforts)
                if(efforts < effort):
                    effort=efforts
                    tasks.clear()
                    tasks.append(task)
                elif(efforts==effort):
                    tasks.append(task)
                
            return [tasks,effort]

        #update the cost of project
        def updateCost(cost, durationFinishFisrt, dedication):
            initial_cost=0
            for e in range(employee):

                if(normalize== True):
                    initial_cost = initial_cost + (get_salary(e) * min(1,dedication[e]))
                else:
                    initial_cost = initial_cost + (get_salary(e) * dedication[e])
                    


            return cost+durationFinishFisrt * initial_cost


        #remove task completed
        def removeTask(task,unfinished_task,level):
        # print("removing", task)
            #print("from", unfinished_task)
            unfinished_task.remove(task)

            #update in degree
            dep=get_dependence(task)
            for i in range(dep):
                d=taskDepPos(task)[i]
                level[d] = level[d]-1
            
            level[task] = -6

       
        #penalty
        def infeasibles():
            infeasibleCost = 0
            infeasibleDuration=0
            for i in range(task):
                infeasibleDuration= infeasibleDuration + get_effort(i)
                for emp in range(employee):
                    infeasibleCost = infeasibleCost + (get_salary(emp) * get_effort(i))
            infeasibleDuration= infeasibleDuration *k

            return 2*((costWeight*infeasibleCost) + (durationWeight*infeasibleDuration))

        #get missing skills
        def get_missing_skills(task,phe):
            missing=0
            kin =[]
            #for i in range(task):
            d = [row[task] for row in phe]
            #print(d)
            for p in range(len(d)):
                teamS=[]
                if d[p]>0:
                    a=p+1
                    #for k, v in eSkil.items():
                    teamS= teamS + eSkil[a]
                    kin.append(teamS)
                else:
                    kin.append([])
            
            result = sum(kin, [])
            #print(list(set(result)))
            for sk in reqSk[task+1]:
                if sk not in result:
                    missing=missing+1
            kin=[]    
            return missing

        def get_effort(eff):
            return required_efforts[eff]

        def decode(geno,k):
            phenotype = []
            phenotype = np.true_divide(geno,k)
           
            return phenotype

        def check_overwork(overwork,durationFirst, dedEmployee,normalize):
            
            overtime=0
            for i in range(employee):
                countOverwork= dedEmployee[i] - 1
                if countOverwork > 0:
                    overtime = overtime + countOverwork
                    #print("overtime::", overtime)
            return overwork + durationFirst * overtime


        #calculate fitness
        def get_fit(cost, duration,reqsk,wReqsk, overw):
            if(reqsk==0 and overw==0):
                return durationWeight*(round(duration,1)) + costWeight *(round(cost,1)) 
            elif(reqsk > 0):
                return wReqsk * reqsk
            else:
                return wReqsk +overw

        #######################################
        #calculation
       #evaluate function
        def evaluate(task,geno):
            
            phe=[]
            phe=decode(geno,k)
            
            ph=phe.copy()
            unfinished_task=[0]*task
            totalDedicationTask = [0]*task
            SumEmployee=[0] *employee
            required_effort=requiredE.copy()
            start=[0]*task
            finish=[0]*task
            cost=0
            duration=0
            overworks=0
            normalize=False
            reqsk=0
            level=get_precedence()
            wReqsk=infeasibles()
            
            
            #determine unfinished task
            for i in range(task):
                unfinished_task[i]=i

        

            

            while (unfinished_task):

                currentTask=indepTask(level)
            # print(currentTask)

                if(len(currentTask)==0):
                    cost=-1
                    duration=-1
                    print("Error cannot start task")
                    break

                for e in range(employee):
                    """"""
                    SumEmployee[e]=getDedicationEmployee(e,currentTask,phe)
                z=0
                while z<(len(currentTask)):
                    normalize=False
                   
                    task=currentTask[z]
                    
                    totalDedicationTask[task]=0
                    for e in range(employee):
                        if(SumEmployee[e] >1):
                            normalize=True
                           
                            totalDedicationTask[task] = totalDedicationTask[task] + getEmployeeTaskded(e,task,phe)/max(1,SumEmployee[e])
                       
                            ph[e][task]= getEmployeeTaskded(e,task,phe)/max(1,SumEmployee[e])
                        else:
                            
                            
                            totalDedicationTask[task] = totalDedicationTask[task] + getEmployeeTaskded(e,task,phe)
                       
                            ph[e][task]= getEmployeeTaskded(e,task,phe)

                    skillSet=get_missing_skills(task,phe)
                    #print("missing skill for:",task, 'is ', skillSet)
                    if(skillSet >0):
                        reqsk=reqsk + skillSet
                        removeTask(task,unfinished_task,level)
                        #print('currentTask', task)
                        currentTask.remove(task)
                        #print("curent tasksecond", task)
                    else:
                        z=z+1

                if(len(currentTask)==0):
                    continue
                
                task_dur=durtoFinishFirst(currentTask,totalDedicationTask,required_effort)
                #print("duration tasks involved", task_dur)
                duration_first = task_dur[1]
                first_task=task_dur[0]
                cost=updateCost(cost,duration_first,SumEmployee)
                duration =duration + duration_first
                #print("my duration", duration)
                overworks=check_overwork(overworks,duration_first,SumEmployee,normalize)
                #print("task at this moment",currentTask)
                #print('overwork at this moment is ;;', overworks)
                for i in range(len(currentTask)):
                    tk = currentTask[i]
                
                    if tk not in first_task:
                        #if(normalize==True):
                        required_effort[tk] = required_effort[tk] - (duration_first * totalDedicationTask[tk])
                        #print("required effort remainig" , tk, " ", required_effort[tk])
                    # print("effort Norm",required_effort)
                        #normalize=False
                    else:
                        required_effort[tk] =0
                        #print("effort unnorm",required_effort)
                        o=preced(tk)
                        #print("precedent scehe", o)
                        if len(o)==0:
                            start[tk]=0
                            finish[tk]=duration
                        else:
                            start[tk]=finish[o[0]]
                            finish[tk]=duration
                        removeTask(tk,unfinished_task,level)
                        #normalize=False
                #print("-----------------------")
            
            #print("overwork at last task", ,  overworks)
            par=(cost,duration,overworks,start,finish,phe,ph)      
            fit=get_fit(cost,duration,reqsk,wReqsk,overworks)
            return fit,par

        ########################################
        #EA running
        class Individual:
            def __init__(self):
                self.genes= []
                self.fitness = 0
                self.costD=[]
                self.fitter=[]
            
                self.genes = np.random.randint(0,k+1,(employee,task))
                # gene= [
                #     [1, 0, 10, 8],
                #     [5, 1, 7, 0],
                #     [2, 0, 2, 0],
                #     [3, 4, 9, 1]
                            
                #              ]
                # self.genes = np.array(gene)
                
            def get_genes(self):
                return self.genes
            
            def get_fitness(self):
                #fitter =[]
                cD=[]
                self.fitter=evaluate(len(self.genes[0]),self.genes)
                self.fitness = self.fitter[0]
                
            
                return self.fitness

            def get_cD(self):
                film=self.fitter
                self.costD=film[1]
                return self.costD


            def __str__(self):
                return self.genes.__str__()

        class Population: 
            def __init__(self, size):
                self.individual = []
                i =0
                while i < size:
                    self.individual.append(Individual())
                    i +=1
            
            def get_individual(self):
                return self.individual
            

        class EA:
            """"""
            @staticmethod
            def evolution(pop):
                return EA.mutate_population(EA.crossover_population(pop))

            @staticmethod
            def crossover_population(pop):
                crossover_pop = Population(0)

                for i in range(NUM_ELITE):
                    crossover_pop.get_individual().append(pop.get_individual()[i])

                i =NUM_ELITE
                while i < POPULATION_SIZE:
                    parent1= EA.tournamnet_pop(pop).get_individual()[0]
                    parent2= EA.tournamnet_pop(pop).get_individual()[0]

                    crossover_pop.get_individual().append(EA.crossover_chrome(parent1, parent2))
                    i +=1
            
                return crossover_pop

            @staticmethod
            def mutate_population(pop):
                for i in range(NUM_ELITE, POPULATION_SIZE):
                    EA.mutate_chrome(pop.get_individual()[i])
                return pop
            
            @staticmethod
            def clone(phe):
                """
                Duplicates the schedule
                """
                return [list(i) for i in phe]
            

            @staticmethod
            def crossover_chrome(parent1,parent2):
                """"""
                crossover_chrome = Individual()
               
                child1 =copy.copy(parent1)
                child2 =copy.copy(parent2)

                if random.random() >= 0.5:
                    for i in range(employee):
                        for j in range(task):
                            if random.random() >= 0.5:
                                crossover_chrome.get_genes()[i][j] = child1.get_genes()[i][j]
                                
                            else:
                                crossover_chrome.get_genes()[i][j] = child2.get_genes()[i][j]
                                
                else:
                    for i in range(employee):
                        if random.random() >= 0.5:
                            crossover_chrome.get_genes()[i] = child1.get_genes()[i]
                           
                        else:
                            crossover_chrome.get_genes()[i] = child2.get_genes()[i]
                            
                
                # if (employee==1):
                #     #print('one employeee mode')
                #     for i in range(employee):
                #         for j in range(task):
                #             if random.random() >= 0.5:
                #                 crossover_chrome.get_genes()[i][j] = child1.get_genes()[i][j]
                #                 #print("after cross at less 0.5:: ", crossover_chrome.get_genes()[i])
                #             else:
                #                 crossover_chrome.get_genes()[i][j] = child2.get_genes()[i][j]
                #                 #print("after cross at greater 0.5:: ", crossover_chrome.get_genes()[i])
                # else:
                #     for i in range(employee):
                #         if random.random() >= 0.5:
                #             crossover_chrome.get_genes()[i] = child1.get_genes()[i]
                #             #print("after cross at less 0.5:: ", crossover_chrome.get_genes()[i])
                #         else:
                #             crossover_chrome.get_genes()[i] = child2.get_genes()[i]
                #             #print("after cross at greater 0.5:: ", crossover_chrome.get_genes()[i])

           

                #child1 = np.copy(parent1)
                # for j, t in enumerate(child1):
                #     t[index:] = parent2[j][index:]
                
                return crossover_chrome
            
            @staticmethod
            def mutate_chrome(individual):
            
                if random.random() < MUTATION_RATE:
                    i = random.randint(0,employee-1)
                    j = random.randint(0,task-1)
                    a = individual.get_genes()[i][j]
                    #print(a)
                    individual.get_genes()[i][j] = choice([i for i in range(0,k+1) if i not in [a]])

            @staticmethod
            def tournamnet_pop(pop):
                """"""
                tournament_pop = Population(0)
                i =0
                while i < TOURNAMENT_SIZE:
                    tournament_pop.get_individual().append(pop.get_individual()[random.randrange(0,POPULATION_SIZE)])
                    i +=1
                tournament_pop.get_individual().sort(key=lambda x: x.get_fitness(), reverse=False)
                return tournament_pop



        def printPop(pop, gen):
            print("\n--------------------------------------------------")
            print("Generation #" , gen, "|lowest cost:", pop.get_individual()[0].get_fitness(), " and cost duration is ::",pop.get_individual()[0].get_cD())
            #print("Goal: ", SCHEDULE)
            print("------------------------------------------------")

            i =0 
            for x in pop.get_individual():
                print("\nsolution #", i , " : \n", x , "| fitness: ", x.get_fitness())
                i +=1


        population = Population(POPULATION_SIZE)
        population.get_individual().sort(key=lambda x: x.get_fitness(), reverse=False)

        xv =[]
        yv =[]
        # gtt=[]
        # printPop(population, 0)

        gen_num = 1
        #while population.get_individual()[0].get_fitness() < 5:
        while gen_num < 10:
            population = EA.evolution(population)
            population.get_individual().sort(key=lambda x: x.get_fitness(), reverse=False)
            #printPop(population, gen_num)
            xv.append(gen_num)
            yv.append(1/population.get_individual()[0].get_fitness())
            gen_num +=1
        #print("\nthis is the fittenshshs\n")
        #print(population.get_individual()[0].get_fitness())#, " and cost duration is ::",population.get_individual()[0].get_cD())
        zxc=population.get_individual()[0].get_cD()
        #print('result ', zxc)
        return zxc
    except:
        error="error running evolutionary algorithm "
        print(error)
