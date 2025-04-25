import pandas as pd
import matplotlib.pyplot as plt

TABLE = pd.read_csv("tabela_despadronizada.csv")

def fix_sex():
    for i, value in enumerate(TABLE['sexo']):
        if value in ("masc", "M"):
            TABLE.at[i, 'sexo'] = "Masculino"
        
        elif value in ("fem", "F"):
            TABLE.at[i, 'sexo'] = "Feminino"

def fix_grades():
    for i in range(100):
        TABLE.at[i, 'nota_matematica'] = TABLE.at[i, 'nota_matematica'].replace(".", ",")
        TABLE.at[i, 'nota_portugues'] = TABLE.at[i, 'nota_portugues'].replace(".", ",")

def add_columns():
    for i in range(100):
        formula = f"({TABLE.at[i, 'nota_matematica'].replace(",", ".")} + {TABLE.at[i, 'nota_portugues'].replace(",", ".")} + ({TABLE.at[i, 'frequencia']} / 10)) / 3"
        media = eval(formula)
        
        TABLE.at[i, 'media'] = '%.1f'%(media)
        TABLE.at[i, 'aprovado'] = "Sim" if media >= 7 else "Não"
        
def approval_chart():
    approved = list(TABLE['aprovado']).count("Sim")
    failed = list(TABLE['aprovado']).count("Não")
    
    plt.pie((approved, failed), labels=('Aprovado', 'Reprovado'), colors=('#0fd408', '#e34444'), autopct='%1.1f%%', wedgeprops={'edgecolor': 'black', 'linewidth': 1}, startangle=210)
    plt.title("SITUAÇÃO DOS ALUNOS", fontsize=23)
    plt.savefig('approval_chart.png')
    plt.clf()
    
def sex_chart():
    masculine = list(TABLE['sexo']).count("Masculino")
    feminine = list(TABLE['sexo']).count("Feminino")
    
    plt.pie((masculine, feminine), labels=('Masculino', 'Feminino'), colors=('skyblue', 'pink'), autopct='%1.1f%%', wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    plt.title("DEMOGRAFIA DOS ALUNOS", fontsize=23)
    plt.savefig('sex_chart.png')
    plt.clf()

def top_grades():
    ids = TABLE['id_aluno']
    names = TABLE['nome']
    grades = TABLE['media']
    
    sorted_grades = list(zip([float(g) for g in grades], [f"(Aluno: {n}, ID: {i})" for i, n in zip(ids, names)]))
    sorted_grades.sort()
    
    sorted_values, sorted_names = zip(*sorted_grades)
    
    plt.figure(figsize=(12, 20))
    plt.subplots_adjust(left=0.3)  
    plot = plt.barh(sorted_names, sorted_values, edgecolor='black', align="center")
    plt.xlabel('Notas')
    plt.ylabel('Alunos')
    
    for i, [bar, value] in enumerate(zip(plot, sorted_values)):
        if i >= 95:
            bar.set_facecolor("gold")
           
        plt.text(value+0.05, bar.get_y() + 0.3, f'{value:.1f}', va='center', ha='left')
    
    plt.title("RANKING DE NOTAS" , fontsize=23)
    
    # Legend
    plot[99].set_label("Top 5")
    plt.legend(fontsize=25)
    
    # Finish
    plt.savefig('grade_ranking.png')
    plt.clf()
    
def top_attendance():
    ids = TABLE['id_aluno']
    names = TABLE['nome']
    attendance = TABLE['frequencia']
    
    sorted_grades = list(zip([float(g) for g in attendance], [f"(Aluno: {n}, ID: {i})" for i, n in zip(ids, names)]))
    sorted_grades.sort()
    
    sorted_values, sorted_names = zip(*sorted_grades)
    
    plt.figure(figsize=(15, 20))
    plt.subplots_adjust(left=0.2)  
    plot = plt.barh(sorted_names, sorted_values, edgecolor='black', color="purple", align="center")
    plt.xlabel('Presença (%)')
    plt.ylabel('Alunos')
    
    for i, [bar, value] in enumerate(zip(plot, sorted_values)):
        if i >= 95:
            bar.set_facecolor("pink")
           
        plt.text(value+0.06, bar.get_y() + 0.3, f'{value:.1f}%', va='center', ha='left')
    
    plt.title("RANKING DE PRESENÇA" , fontsize=23)
    
    # Legend
    plot[99].set_label("Top 5")
    plt.legend(fontsize=25)
    
    # Finish
    plt.savefig('attendance_ranking.png')
    plt.clf()


if __name__ == "__main__":
    fix_sex()
    fix_grades()
    add_columns()
    approval_chart()
    sex_chart()
    top_grades()
    top_attendance()
    TABLE.to_csv("tabela_padronizada.csv", index=False)