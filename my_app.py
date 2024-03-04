import pandas as pd
import os
from numpy.random import randn
import streamlit as st
import matplotlib.pyplot as plt
import openpyxl
from streamlit_card import card
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events
st.set_page_config(
    layout="wide",
    page_title="Resultados da Auditoria de Campo"
)
import zipfile
from zipfile import ZipFile
import io

@st.cache
#@st.cache_data



def load_data():
    caminho_zip = "https://github.com/CLEBER161/streamlit/blob/main"
# Diretório onde deseja extrair os arquivos
    diretorio_destino = "https://github.com/CLEBER161/streamlit/blob/main"

# Extrair os arquivos
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        zip_ref.extractall(diretorio_destino)
    df_data2 = pd.read_excel('https://github.com/CLEBER161/streamlit/blob/main/BASE23.xlsx', engine='openpyxl')
    
    return df_data2







df_data2 = load_data()
st.session_state['df_data2']=df_data2   
col3,col4,col5,col6 =st.columns([0.25,0.25,0.25,0.25],gap="small")
col1, col2=st.columns([0.33,0.33])
col7,col8=st.columns([0.9999,0.0001])



#print(df_data2['DIRETORIA'].value_counts().index)
#print(type(list(df_data2['DIRETORIA'].value_counts().index)))

selected_Dir = st.sidebar.multiselect('Selecione os Meses:',df_data2['MÊS'].value_counts().index,default=list(df_data2['MÊS'].value_counts().index))
df_data2_filtared = df_data2 [
    (df_data2 ['MÊS'].isin(selected_Dir))    
]
selected_Dir = st.sidebar.multiselect('Selecione as Diretorias:',df_data2_filtared['DIRETORIA'].value_counts().index,default=list(df_data2_filtared['DIRETORIA'].value_counts().index))
df_data2_filtared = df_data2 [
    (df_data2 ['DIRETORIA'].isin(selected_Dir))    
]


selected_UF = st.sidebar.multiselect('Selecione as UF:', df_data2_filtared['UF'].value_counts().index,default=list(df_data2_filtared['UF'].value_counts().index))
df_data2_filtared = df_data2_filtared [
    
    (df_data2_filtared ['UF'].isin(selected_UF))    
]

selected_Aud = st.sidebar.multiselect('Selecione as Auditorias:',df_data2_filtared['AUDITORIA'].value_counts().index,default=list(df_data2_filtared['AUDITORIA'].value_counts().index))
df_data2_filtared = df_data2_filtared [
   
    (df_data2_filtared ['AUDITORIA'].isin(selected_Aud))   
]

selected_Cat = st.sidebar.multiselect('Selecione as Categorias:', df_data2_filtared['CATEGORIA'].value_counts().index,default=list(df_data2_filtared['CATEGORIA'].value_counts().index))


# Aplicar filtros ao DataFrame
df_data2_filtared = df_data2_filtared [
 
    (df_data2_filtared ['CATEGORIA'].isin(selected_Cat))
]






def Tabelas(x):
    
    #print(x)
    RESULTADO=df_data2_filtared
    #RESULTADO=df_data2_filtared[['ID TECNICO','VALOR','DATA','AUDITORIA','CATEGORIA','ITENS']]
        #RESULTADO2 = RESULTADO.loc[RESULTADO['AUDITORIA'].isin(AUDITORIA)]
    #RESULTADO2=RESULTADO[RESULTADO['AUDITORIA'].isin(AUDITORIA)]
    RESULTADO2=df_data2_filtared[['ID TECNICO','VALOR','DATA','AUDITORIA','CATEGORIA','ITENS','UF','DIRETORIA',"NÚMERO DO BILHETE DE ATIVIDADE (BA)","PILAR"]]
    # RESOLVER O PROBLEMAS DOS FILTROS
    #RESULTADO['AUDITORIA'].isin(AUDITORIA)

    TUDO=["CONFORME","NÃO CONFORME"]
    RESULTADO_C=RESULTADO2.loc[RESULTADO2['VALOR']=="CONFORME"]
    RESULTADO_NC=RESULTADO2.loc[RESULTADO2['VALOR']=="NÃO CONFORME"]
    RESULTADO_T=RESULTADO2.loc[RESULTADO2['VALOR'].isin(TUDO)]

    CONFORME = pd.DataFrame({})
    NÃO_CONFORME = pd.DataFrame({})

    CONFORME=RESULTADO_C[(RESULTADO_C['VALOR']=="CONFORME")]
    NÃO_CONFORME=RESULTADO_NC[(RESULTADO_NC['VALOR']=="NÃO CONFORME")]
    #print(CONFORME.head)
    #TOTAL_ITENS=
    TOTAL_BA=RESULTADO_T.groupby(x)['NÚMERO DO BILHETE DE ATIVIDADE (BA)'].nunique()
    TOTAL_TECNICOS=RESULTADO_T.groupby(x)['ID TECNICO'].nunique()

    #print(RESULTADO_C)
    #print(RESULTADO_NC)
    #print(type(NÃO_CONFORME))
    CONFORME1 = RESULTADO_C[[x,'VALOR']]
    NÃO_CONFORME1 =RESULTADO_NC[[x,'VALOR']]
    CONFORME2 = CONFORME1.groupby(x)['VALOR'].size()
    NÃO_CONFORME2 =NÃO_CONFORME1.groupby(x)['VALOR'].size()

    GER= NÃO_CONFORME2/(CONFORME2 + NÃO_CONFORME2)*100
    tabela1=GER.to_frame()
    # Preencher valores nulos com um valor padrão, como 0
    tabela1 = tabela1.fillna(0)
    tabela1 ['VALOR']=pd.to_numeric(tabela1 ["VALOR"])
    
    tabela1 = pd.merge(tabela1, TOTAL_TECNICOS, left_index=True, right_index=True, how='left')
    tabela1 = pd.merge(tabela1, TOTAL_BA, left_index=True, right_index=True, how='left')
    tabela1 = tabela1.sort_values(by='VALOR', ascending=False)
    #print(tabela1)
    tabela1['VALOR']=tabela1['VALOR'].apply(lambda x: f'{x * 1:.2f}%')
    tabela1 = tabela1.rename(columns={'VALOR': '% NÃO CONFORMIDADE'})
    #print(tabela1)

  

   
    
    return tabela1,RESULTADO


def Tabelas_pilar(y):
   
    RESULTADO=df_data2_filtared
 
    RESULTADO2=df_data2_filtared[['ID TECNICO','VALOR','DATA','AUDITORIA','CATEGORIA','ITENS','UF','DIRETORIA',"NÚMERO DO BILHETE DE ATIVIDADE (BA)","PILAR"]]
   
    NC=['NÃO CONFORME']
    C=['CONFORME']
    TUDO=["CONFORME","NÃO CONFORME"]
    RESULT_C=RESULTADO2.loc[RESULTADO2['VALOR'].isin(C)&RESULTADO2['PILAR'].isin(y)]
    RESULT_NC=RESULTADO2.loc[RESULTADO2['VALOR'].isin(NC)&RESULTADO2['PILAR'].isin(y)]
    RESULT_T=RESULTADO2.loc[RESULTADO2['VALOR'].isin(TUDO)&RESULTADO2['PILAR'].isin(y)]

  
    
    CONFORME = (RESULT_T['VALOR'] == "CONFORME").sum()

    NÃO_CONFORME = (RESULT_T['VALOR'] == "NÃO CONFORME").sum()

    #print(type(NÃO_CONFORME))
  
    #print(RESULT_C)
    #print(RESULT_NC)
    GERAL= NÃO_CONFORME/(CONFORME + NÃO_CONFORME)*100
    
    #print(GERAL)

    return GERAL






NO_NE=['PI','AL','PE','PA','BA','CE','MA','AM','SE','RN']
SUL_SUD=['SC','PR','RJ','RS']
PILAR_GENTE=['PILAR - GENTE']
PILAR_SEGURANÇA=['PILAR - SEGURANÇA']
PILAR_EXP=['PILAR - EXPERIÊNCIA DO CLIENTE']



######################GRAFICOS DE BARRAS COM LINHAS###################

GERAL1=Tabelas("UF")[0]
GERAL1=GERAL1.loc[GERAL1.index.isin(NO_NE)]


print(GERAL1)
#ax.invert_yaxis()


categorias =GERAL1.index
barras = GERAL1['ID TECNICO']
barrasBA = GERAL1['NÚMERO DO BILHETE DE ATIVIDADE (BA)']
linhas = GERAL1['% NÃO CONFORMIDADE']
#print(GERAL1)

#categorias, linhas = zip(*sorted(zip(categorias, linhas), key=lambda x: x[1], reverse=True))outside
print(GERAL1)
# Crie o gráfico de barras
fig = go.Figure()

# Adicione as barrastop center
fig.add_trace(go.Bar(x=categorias, y=barras,text=barras,  marker_color='orange', name='Total de Técnicos',textposition='inside'))
fig.add_trace(go.Bar(x=categorias, y=barrasBA,text=barrasBA,  marker_color='gray', name='Total de BA',textposition='inside'))

# Adicione a linha
fig.add_trace(go.Scatter(x=categorias, y=linhas,text=GERAL1['% NÃO CONFORMIDADE'],  mode='lines', line=dict(color='purple'), name='% NC',
                        texttemplate=GERAL1['% NÃO CONFORMIDADE']))
#fig.add_annotation(x=categorias, y=linhas,text=str(GERAL1['% NÃO CONFORMIDADE'].value_counts().index))
#fig.update_traces(texttemplate=GERAL1['% NÃO CONFORMIDADE'])
fig.update_layout(
    title='% de NC',
    xaxis_title='Categoria',
    yaxis_title='Valores',
    paper_bgcolor='rgba(0,0,0,0)',  # Define o fundo transparente
    plot_bgcolor='rgba(0,0,0,0)',  # Define o fundo transparente
     font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=16,  # Tamanho da fonte
        color="darkslategray"  # Cor da fonte
    ),
    width=400,
    height=400
)


# Personalize o layout com fundo transparente


GERAL2=Tabelas("UF")[0]
GERAL2=GERAL2.loc[GERAL2.index.isin(SUL_SUD)]
print(GERAL2)


categorias2 =GERAL2.index
barras2 = GERAL2['ID TECNICO']
barrasBA2 = GERAL2['NÚMERO DO BILHETE DE ATIVIDADE (BA)']
linhas2 = GERAL2['% NÃO CONFORMIDADE']
#print(GERAL2)

#categorias2, linhas2 = zip(*sorted(zip(categorias2, linhas2), key=lambda x: x[1], reverse=True))
# Crie o gráfico de barras
fig2 = go.Figure()

# Adicione as barras
fig2.add_trace(go.Bar(x=categorias2, y=barras2, text=barras2, marker_color='orange', name='Total de Técnicos',textposition='inside'))
fig2.add_trace(go.Bar(x=categorias2, y=barrasBA2,text=barrasBA2,  marker_color='gray', name='Total de BA',textposition='outside'))

# Adicione a linha
fig2.add_trace(go.Scatter(x=categorias2, y=linhas2,text=GERAL2['% NÃO CONFORMIDADE'], mode='lines',  line=dict(color='purple'), 
                name='% NC',texttemplate=GERAL2['% NÃO CONFORMIDADE']))
#fig2.add_annotation(x=categorias2, y=linhas2,text=str(GERAL2['% NÃO CONFORMIDADE'].value_counts().index))
# Personalize o layout com fundo transparente
#fig2.update_traces(texttemplate=GERAL2['% NÃO CONFORMIDADE'])
fig2.update_layout(
    title='% de NC',
    xaxis_title='Categoria',
    yaxis_title='Valores',
    paper_bgcolor='rgba(0,0,0,0)',  # Define o fundo transparente
    plot_bgcolor='rgba(0,0,0,0)', 
    #width=10,
    #height=10,  # Define o fundo transparente
     font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=16,  # Tamanho da fonte
        color="darkslategray"  # Cor da fonte
    ),
    width=400,
    height=400
)



##GRAAFICO DE ITENS



GERAL31=Tabelas("ITENS")[0]

#GERAL3 = GERAL3.sort_values(by='% NÃO CONFORMIDADE', ascending=False)
GERAL3=GERAL31.head(10)

#start = st.slider('Selecione a posição inicial:', min_value=0, max_value=len(GERAL3) - 10, value=0)
#total_tecnicos=len(GERAL1)
# Criar gráfico
#fig9, ax = plt.subplots()
#ax.bar(GERAL3.index[start:start+10], GERAL3['% NÃO CONFORMIDADE'][start:start+10], GERAL3['ID TECNICO'][start:start+10],GERAL3['NÚMERO DO BILHETE DE ATIVIDADE (BA)'][start:start+10])



categorias3 =GERAL3.index
barras3 = GERAL3['ID TECNICO']
barrasBA3 = GERAL3['NÚMERO DO BILHETE DE ATIVIDADE (BA)']
linhas3 = GERAL3['% NÃO CONFORMIDADE']

#categorias3, linhas3 = zip(*sorted(zip(categorias3, linhas3), key=lambda x: x[1], reverse=True))
# Crie o gráfico de barras
fig7 = go.Figure()

# Adicione as barras
fig7.add_trace(go.Bar(x=categorias3, y=barras3, text=barras3, marker_color='orange', name='Total de Técnicos'))
fig7.add_trace(go.Bar(x=categorias3, y=barrasBA3,text=barrasBA3,  marker_color='gray', name='Total de BA'))

# Adicione a linha
fig7.add_trace(go.Scatter(x=categorias3, y=linhas3,text=GERAL3['% NÃO CONFORMIDADE'], mode='lines',  line=dict(color='purple'), name='% NC'
                          ,texttemplate=GERAL3['% NÃO CONFORMIDADE']))

# Personalize o layout com fundo transparente
fig7.update_layout(
    title='% de NC',
    xaxis_title='Categoria',
    yaxis_title='Valores',
    paper_bgcolor='rgba(0,0,0,0)',  # Define o fundo transparente
    plot_bgcolor='rgba(0,0,0,0)',  # Define o fundo transparente
     font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=16,  # Tamanho da fonte
        color="darkslategray"  # Cor da fonte
    )
)







#################COLUNA3 GRAFICO DE PIZZAS#########################
####3PIZZA GERAL
Pilar_Geral=Tabelas_pilar(PILAR_GENTE+PILAR_SEGURANÇA+PILAR_EXP)
NC=Pilar_Geral
C=(Pilar_Geral-100)*-1


# Dados de exemplo
categorias = ['%NC','C']
valores_cinza = [NC,C]
cores=['orange','gray']
#valores_cinza = [30, 70]

# Crie o gráfico de pizza
fig3 = go.Figure(data=go.Pie(
    labels= categorias,
        values= valores_cinza,
        marker_colors=cores)
)

fig3.update_layout(
    #title='Gráfico de Pizza com Dois Resultados',
    font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=18,  # Tamanho da fonte
        color="darkslategray",  # Cor da fonte
         
    ),
    width=300,
    height=300
)

# Exiba o gráfico







#########PIZZA PILAR GENTE

Pilar_Gente=Tabelas_pilar(PILAR_GENTE)
NC1=Pilar_Gente
C1=(Pilar_Gente-100)*-1


# Dados de exemplo
categorias = ['%NC','C']
valores_cinza = [NC1,C1]
cores=['orange','gray']
#valores_cinza = [30, 70]

# Crie o gráfico de pizza
fig4 = go.Figure(data=go.Pie(
    labels= categorias,
        values= valores_cinza,
        marker_colors=cores)
)

fig4.update_layout(
    #title='Gráfico de Pizza com Dois Resultados',
    font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=18,  # Tamanho da fonte
        color="darkslategray" , # Cor da fonte
       
    ),
    width=300,
    height=300
)


#########PIZZA PILAR SEGURANÇA

Pilar_Gente=Tabelas_pilar(PILAR_SEGURANÇA)
NC2=Pilar_Gente
C2=(Pilar_Gente-100)*-1


# Dados de exemplo
categorias = ['%NC','C']
valores_cinza = [NC2,C2]
cores=['orange','gray']
#valores_cinza = [30, 70]

# Crie o gráfico de pizza
fig5 = go.Figure(data=go.Pie(
    labels= categorias,
        values= valores_cinza,
        marker_colors=cores)
)

fig5.update_layout(
   # title='Gráfico de Pizza com Dois Resultados',
    font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=18,  # Tamanho da fonte
        color="darkslategray" , # Cor da fonte
       
    ),
    width=300,
    height=300
)


#########PIZZA PILAR EXPERIENCIA DO CLIENTE


Pilar_Gente=Tabelas_pilar(PILAR_EXP)
NC3=Pilar_Gente
C3=(Pilar_Gente-100)*-1


# Dados de exemplo
categorias = ['%NC','C']
valores_cinza = [NC3,C3]
cores=['orange','gray']
#valores_cinza = [30, 70]

# Crie o gráfico de pizza
fig6 = go.Figure(data=go.Pie(
    labels= categorias,
        values= valores_cinza,
        marker_colors=cores)
)

fig6.update_layout(
    #title='Gráfico de Pizza com Dois Resultados',
     font=dict(
        family="Arial",  # Pode escolher a fonte desejada
        size=18,  # Tamanho da fonte
        color="darkslategray",  # Cor da fonte
       
    ),
    width=300,
    height=300
)




#selected_points = plotly_events(fig)

# Can write inside of things using with!
#with st.expander('Plot'):
    #fig = px.line(x=[1], y=[1])
    #selected_points = plotly_events(fig)

def subheader_custom_font(text, font_size):
    st.markdown(f"<h3 style='font-size:{font_size}px;'>{text}</h3>", unsafe_allow_html=True)

# Uso da função customizada
subheader_custom_font("Este é um subcabeçalho", 24)

col3.subheader("Resultado Geral")
#col2.write(RESULTADO)
col3.plotly_chart(fig3, use_container_width=True)

col4.subheader("<h3 style='color:blue;'>Resultado Pilar-Gente</h3>")
col4.plotly_chart(fig4, use_container_width=True)

col5.subheader("<h3 style='color:blue;'>Resultado Pilar-Segurança</h3>")
col5.plotly_chart(fig5, use_container_width=True)

col6.subheader("<h3 style='color:blue;'>Resultado Pilar-Expereiência do Cliente</h3>")
col6.plotly_chart(fig6, use_container_width=True)


col1.subheader("DIRETORIA NO/NE")
col1.plotly_chart(fig, use_container_width=True)

#st.write("Total de Tecnicos Auditados: "+ str(total_tecnicos))
#col1.write(GERAL1)

col2.subheader("DIRETORIA SUL/SUD")
#col2.write(RESULTADO)
col2.plotly_chart(fig2, use_container_width=True)




col7.subheader("% NC por Item")
#col2.write(RESULTADO)
col7.plotly_chart(fig7, use_container_width=True)



#col3.write(NC)
#col3.write(C)

#st.write(GERAL1)
#st.bar_chart(GERAL1['% NÃO CONFORMIDADE'])

#st.write(RESULTADO)
