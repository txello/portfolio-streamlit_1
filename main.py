import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Анализ Финансового Портфеля")

uploaded_file = st.file_uploader("Загрузите CSV файл с данными о портфеле", type=["csv"])

@st.cache_data
def example_file():
    return pd.read_csv("test.csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    expected_columns = {'Company', 'Quantity', 'Purchase Price', 'Current Price'}
    if not expected_columns.issubset(df.columns):
        st.error(f"Ошибка: Файл должен содержать следующие колонки: {expected_columns}")
    else:
        st.subheader("Загруженные данные:")
        st.write(df)

        df['Profit'] = (df['Current Price'] - df['Purchase Price']) * df['Quantity']
        df['Profit (%)'] = ((df['Current Price'] - df['Purchase Price']) / df['Purchase Price']) * 100

        total_profit = df['Profit'].sum()

        st.subheader("Расчеты:")
        st.write(f"Общий доход по портфелю: {total_profit:.2f}₽")
        st.write("Доход по каждой компании (в процентах):")
        st.write(df[['Company', 'Profit', 'Profit (%)']])

        st.subheader("График прибыли по компаниям")
        plt.figure(figsize=(10, 6))
        plt.bar(df['Company'], df['Profit'], color='skyblue')
        plt.xlabel('Company')
        plt.ylabel('Profit (₽)')
        plt.title('Profit per Company')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)
        
        st.subheader("Распределение активов")
        plt.figure(figsize=(8, 8))
        plt.pie(df['Quantity'], labels=df['Company'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Asset Allocation by Quantity')
        plt.axis('equal')
        st.pyplot(plt)

else:
    st.info("Пожалуйста, загрузите CSV файл с данными о портфеле, или, используйте пример файла ниже:")
    with open("example.csv", "rb") as file:
        st.download_button(
            label="Пример CSV",
            data=file,
            file_name="example.csv",
            mime="text/csv",
        )