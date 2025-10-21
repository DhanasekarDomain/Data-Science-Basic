import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from matplotlib import pyplot
from scipy.stats import norm
import seaborn as sb

class univeriate():
    
    def quanqual(datapool):
        quan=datapool.select_dtypes(include=['number']).columns
        qual=datapool.select_dtypes(exclude=['number']).columns
        return quan,qual              
        
    def Preprocessing_Data(datapool,quan,qual):
        imp_mean = SimpleImputer(missing_values=np.nan,strategy='constant',fill_value=0).fit(datapool[quan])
        df_quan=imp_mean.transform(datapool[quan])
        df_quan=pd.DataFrame(df_quan,columns=quan)
        datapool[quan]=df_quan
       
        imp_mean2 = SimpleImputer(missing_values=np.nan,strategy="most_frequent").fit(datapool[qual])
        df_qual=imp_mean2.transform(datapool[qual])
        df_qual=pd.DataFrame(df_qual,columns=qual)
        datapool[qual]=df_qual
        return datapool[quan],datapool[qual]
        
    def Descriptive_Table (quan,datapool):
        descriptive=pd.DataFrame(index=["mean","median","mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","Min","Max",
                                        "Lesser","Greater","Kurtosis","Skewness","Variance","Standard deviation"],columns=quan)
        for ColumnName in quan:
            descriptive[ColumnName]["mean"]=datapool[ColumnName].mean()
            descriptive[ColumnName]["median"]=datapool[ColumnName].median()
            descriptive[ColumnName]["mode"]=datapool[ColumnName].mode()[0]
            descriptive[ColumnName]["Q1:25%"]=datapool.describe()[ColumnName]["25%"]
            descriptive[ColumnName]["Q2:50%"]=datapool.describe()[ColumnName]["50%"]
            descriptive[ColumnName]["Q3:75%"]=datapool.describe()[ColumnName]["75%"]
            descriptive[ColumnName]["99%"]=np.percentile(datapool[ColumnName],99)
            descriptive[ColumnName]["Q4:100%"]=datapool.describe()[ColumnName]["max"]
            descriptive[ColumnName]["IQR"]=datapool.describe()[ColumnName]["75%"]-datapool.describe()[ColumnName]["25%"]
            descriptive[ColumnName]["Min"]=datapool[ColumnName].min()
            descriptive[ColumnName]["Max"]=datapool[ColumnName].max()
            descriptive[ColumnName]["Lesser"]=datapool.describe()[ColumnName]["25%"]-(1.5*descriptive[ColumnName]["IQR"])
            descriptive[ColumnName]["Greater"]=datapool.describe()[ColumnName]["75%"]+(1.5*descriptive[ColumnName]["IQR"])
            descriptive[ColumnName]["Kurtosis"]=datapool[ColumnName].kurtosis()
            descriptive[ColumnName]["Skewness"]=datapool[ColumnName].skew()
            descriptive[ColumnName]["Variance"]=datapool[ColumnName].var()
            descriptive[ColumnName]["Standard deviation"]=datapool[ColumnName].std()
        return  descriptive

    def Indentify_Outlier(quan,descriptive):
        LesserOutlier=[]
        GreaterOutlier=[]
        for ColumnName in quan:
            if (descriptive[ColumnName]["Min"]<descriptive[ColumnName]["Lesser"]):
                LesserOutlier.append(ColumnName)        
            if (descriptive[ColumnName]["Max"]>descriptive[ColumnName]["Greater"]):
                GreaterOutlier.append(ColumnName)
        return LesserOutlier,GreaterOutlier

    def Replace_Outlier(LesserOutlier,GreaterOutlier,descriptive,datapool):
        for ColumnName in LesserOutlier:    
            datapool[ColumnName][datapool[ColumnName]<descriptive[ColumnName]["Lesser"]]=descriptive[ColumnName]["Lesser"]
        for ColumnName in GreaterOutlier: 
            datapool[ColumnName][datapool[ColumnName]>descriptive[ColumnName]["Greater"]]=descriptive[ColumnName]["Greater"]
        return ColumnName
    
    def Frequency(ColumnName,datapool):
            frequency_table=pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","Cumlative_Frequency"])
            frequency_table["Unique_Values"]=datapool[ColumnName].value_counts().index
            frequency_table["Frequency"]=datapool[ColumnName].value_counts().values
            frequency_table["Relative_Frequency"]=(frequency_table["Frequency"]/103)
            frequency_table["Cumlative_Frequency"]= frequency_table["Relative_Frequency"].cumsum()
            return frequency_table
        
    def get_pdf_probability(datapool,startrange,endrange):
        ax = sb.distplot(datapool,kde=True,kde_kws={'color':'Blue'},color='Green')
        pyplot.axvline(startrange,color='Red')
        pyplot.axvline(endrange,color='Red')

        print(f'Mean={datapool.mean():.3f}, Standard Deviation={datapool.std():.3f}')

        dist = norm(datapool.mean(),datapool.std())
    
        values = range(startrange,endrange)
        probabilities = [dist.pdf(value) for value in values]    
        prob=sum(probabilities)
        print(f"The area between range({startrange},{endrange}):{prob:.4f}")
        return prob

    def STDND_z_score (datapool):
        mean = datapool.mean()
        std = datapool.std()       
        z_scores = (datapool - mean) / std     
        sb.distplot(z_scores, kde=True,kde_kws={'color':'Blue'},color='Green')
        return z_scores