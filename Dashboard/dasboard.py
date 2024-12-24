import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import streamlit as st

def create_customer_df(df):
    customer_df = df[df['order_status'].isin(['delivered', 'shipped', 'invoiced', 'processing', 'created'])]
    return customer_df

def create_customer_info(df):
    customer_count = df['customer_id'].nunique()
    return customer_count

def create_revenue_info(df):
    revenue_sum = round(df['payment_value'].sum(),2)
    return revenue_sum

def create_ordered_info(df):
    order_sum = df[df['order_status']=='delivered']['order_id'].nunique()
    return order_sum

def create_geo_df(main_df, geo_shape):
    geo_shape_gpd =  geo_shape[['geometry', 'name', 'sigla']]
    geo_df = geo_shape_gpd.merge(main_df, left_on='sigla', right_on='customer_state', how='left')
    
    geo_df = geo_df.groupby('sigla').agg({
    'name' : 'unique',
    'customer_id': 'nunique',
    'payment_value' : 'sum',
    'geometry': 'first'
    }).reset_index()
    geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry')
    return geo_df

def create_geo_customer(df):
    fig, ax= plt.subplots()
    df.plot(column='customer_id', cmap='OrRd',ax = ax, 
                       figsize=(10, 10), legend=True, 
                       edgecolor='#9AA6B2', 
                       legend_kwds={'shrink': 0.7})
    
    max_count = df[df['customer_id'] == df['customer_id'].max()]
    low_count = df[df['customer_id'] == df['customer_id'].min()]
    point_df = pd.concat([max_count,low_count])
    for idx, point in point_df.iterrows():
        X, y = point['geometry'].centroid.x , point['geometry'].centroid.y  
        
        ax.plot(X, y, marker='o', color='black', markersize=5)
        ax.text(X,y, point['name'], fontsize=10, color='black', ha='center', verticalalignment='top')
    
    ax.set_title('Distribusi Pelanggan', fontsize=14, pad=20)    
    ax.set_xticks([])  
    ax.set_yticks([])
    st.pyplot(fig)

def create_bar_customer(df):
    df['name'] = df['name'].astype(str)
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    sns.barplot(x='customer_id', y='name', data=df.head().sort_values(by='customer_id',ascending=False), ax=ax[0], palette=colors)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Jumlah Pelanggan", fontsize=30, labelpad=20)
    ax[0].set_title("Kota Pelanggan Terbanyak", loc="center", fontsize=50, pad=30)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)
    
    sns.barplot(x='customer_id', y='name', data=df.head().sort_values(by='customer_id'), ax=ax[1], palette=colors)
    ax[1].invert_xaxis()
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Jumlah Pelanggan", fontsize=30, labelpad=20)
    ax[1].set_title("Kota Pelanggan Terkecil", loc="center", fontsize=50, pad=30)
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)
    st.pyplot(fig)
    
def create_daily_revenue_df(df):
    daily_revenue = df.resample(rule='D', on='order_approved_at').agg({
        'payment_value'  : 'sum'
    }).reset_index()
    return daily_revenue

def daily_revenue_plot(df):
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(df['order_approved_at'], df['payment_value'], linestyle='-', marker='o')
    ax.set_title("Revenue per Hari", loc="center", pad='20', fontsize='15')
    plt.ylim(bottom=0)
    st.pyplot(fig)
    
def create_monthly_revenue_df(df):
    monthly_revenue = df.resample(rule='M', on='order_approved_at').agg({
        'payment_value' : 'sum'
    }).reset_index()
    monthly_revenue['month'] = monthly_revenue['order_approved_at'].dt.strftime('%B')
    return monthly_revenue

def monthly_revenue_plot(df):
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(df['month'], df['payment_value'], linestyle='-', marker='o')
    ax.set_title("Revenue per Bulanan Tahun 2018", loc="center", pad='20', fontsize='15')
    ax.ticklabel_format(style='plain', axis='y')
    plt.ylim(bottom=0)
    st.pyplot(fig)
    
def create_daily_ordered_df(df):
    filter_order = df[df['order_status']=='delivered']
    ordered_df = filter_order.resample(rule='D', on='order_approved_at').agg({
    'order_id' : 'nunique'
    }).reset_index()
    return ordered_df

def daily_ordered_plot(df):
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(df['order_approved_at'], df['order_id'], linestyle='-', marker='o')
    ax.set_title('Total Pengiriman yang Berhasil per Hari', loc='center', pad='20', fontsize='15')
    plt.ylim(bottom=0)
    st.pyplot(fig)
    
def create_monthly_ordered_df(df):
    monthly_ordered_df = df.resample(rule='M', on='order_approved_at').agg({
        'order_id' : 'nunique'
    }).reset_index()
    monthly_ordered_df['month'] = monthly_ordered_df['order_approved_at'].dt.strftime('%B')
    return monthly_ordered_df
    
def monthly_ordered_plot(df):
    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(df['month'], df['order_id'], linestyle='-', marker='o')
    ax.set_title('Total Pengiriman yang Berhasil per Bulan', loc='center', pad='20', fontsize='15')
    plt.ylim(bottom=0)
    st.pyplot(fig)

def create_type_customer_df(df):
    type_customer = df['payment_type'].value_counts().reset_index()
    return type_customer

def create_type_customer_bar(df):
    colors = ['#A8CD89' if value == df['count'].max() else '#DBD3D3' for value in df['count']]

    fig, ax = plt.subplots(figsize=(15, 7))
    sns.barplot(x='payment_type', y='count', data=df, palette=colors, ax=ax)
    ax.set_title('Demografi Pelanggan Berdasarkan Tipe Pembayaran', loc='center', pad=20, fontsize=15)
    ax.set_xlabel('Jenis Pembayaran', fontsize=14, labelpad=20)
    ax.set_ylabel('Jumlah Transaksi', fontsize=14, labelpad=20)
    st.pyplot(fig)

# Load dataframe
all_df = pd.read_csv('Dashboard/main_data.csv')
geo_json = gpd.read_file('Dashboard/brazil-states.geojson')
  
month_column = all_df[['order_purchase_timestamp','order_approved_at',
                       'order_delivered_carrier_date','order_delivered_customer_date',
                       'order_estimated_delivery_date']]

#menukar tipe data
for i in month_column:
    all_df[i] = pd.to_datetime(month_column[i])
    
min_month = all_df['order_approved_at'].min()
max_month = all_df['order_approved_at'].max()

with st.sidebar:
    #input tanggal awal
    start_date = st.date_input(
        label='Input tanggal awal :',
        min_value=min_month,
        max_value=max_month,
        value=min_month)
    
    #input tanggal akhir
    end_date = st.date_input(
        label='Input tanggal akhir :',
        min_value=min_month,
        max_value=max_month,
        value=max_month)
    
main_df= all_df[(all_df['order_approved_at'] >= str(start_date)) & (all_df['order_approved_at'] <=str(end_date))]

#set dataframe
customer_df = create_customer_df(main_df)
geo_df = create_geo_df(main_df, geo_json)
daily_payment_df = create_daily_revenue_df(customer_df)
monthly_revenue_df = create_monthly_revenue_df(daily_payment_df)
daily_ordered_df = create_daily_ordered_df(customer_df)
monthly_ordered_df = create_monthly_ordered_df(customer_df)
type_customer_df = create_type_customer_df(main_df)

#title
st.header("Dicoding Transport")
st.subheader("Daily Report")

#colom menampilkan simple report
col1, col2, col3= st.columns(3)

with col1:
    customer_count = create_customer_info(customer_df)
    st.metric('Total Pelanggan', customer_count)
    
with col2:
    order_sum = create_ordered_info(customer_df)
    st.metric('Total Orderan', order_sum)
    
with col3: 
    revenue_sum = create_revenue_info(customer_df)
    revenue_sum = f"${revenue_sum:,.2f}"
    st.metric('Total Pendapatan', revenue_sum)
   
       
#demografi pelanggan 
st.subheader('\nDemografi Pelanggan')  
col1, col2, col3 = st.columns(3)
with col1:
    pelanggan_provinsi = st.button('Provinsi')
with col2:
    pelanggan_provinsi_bar_plot = st.button('Provinsi (bar)')
with col3:
    tipe_pembayaran = st.button('Tipe Pembayaran')
    
    
if pelanggan_provinsi:
    create_geo_customer(geo_df)
elif pelanggan_provinsi_bar_plot:
    create_bar_customer(geo_df)
elif tipe_pembayaran:
    create_type_customer_bar(type_customer_df)
else:   
    create_geo_customer(geo_df)
    
#peforma penjualan dan pendapatan
st.subheader('\nPeforma pendapatan dan pengiriman yang berhasil')
col1, col2, col3, col4 = st.columns(4)
with col1:
    penjualan_harian = st.button('Revenue Harian')
with col2:
    penjualan_bulanan = st.button('Revenue Bulanan')
with col3:
    pengiriman_harian = st.button('Pengiriman Harian')
with col4:
    pengiriman_bulanan = st.button('Pengiriman Bulanan')
    
if penjualan_harian:
    st.markdown("### Note:")
    st.write("Disarankan untuk menginput data dengan rentang waktu yang pendek")
    daily_revenue_plot(daily_payment_df)
elif penjualan_bulanan:
    st.markdown("### Note:")
    st.write("Disarankan untuk menginput data dengan rentang bulan yang panjang")
    monthly_revenue_plot(monthly_revenue_df)
elif pengiriman_harian:
    st.markdown("### Note:")
    st.write("Disarankan untuk menginput data dengan rentang waktu yang pendek")
    daily_ordered_plot(daily_ordered_df)
elif pengiriman_bulanan:
    st.markdown("### Note:")
    st.write("Disarankan untuk menginput data dengan rentang bulan yang panjang")
    monthly_ordered_plot(monthly_ordered_df)
else:   
    st.markdown("### Note:")
    st.write("Harap pilih salah satu jenis data untuk menampilkan grafik.")




