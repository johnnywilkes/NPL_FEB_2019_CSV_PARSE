# __Johnny's CSV Report Parser__

> This document uses Markdown.  Please view on Github (https://github.com/johnnywilkes/NPL_FEB_2019_CSV_PARSE) or use the following for viewing: https://stackedit.io/app#

## ___Overall Program Idea___

>  **Please note that this program uses the [Pandas](http://pandas.pydata.org) module.  If you don't have the Pandas module installed, it will prompt and error and quit.  Run `pip install pandas` to install.**

> **This program also assumes that you have selected the csv to parse via command line argument or that you are going to parse a default file ('NPL_Feb_Inventory.csv') in the same directory as the script.**

This challenge took a little while for me to wrap my head around.  The goal was to parse a large csv and print the number of unique vendor/model/software version combinations (along with EoS information) such as:

```
Count  Vendor    Model                Software             End of Service      
1      Cisco     CISCO3925-CHASSIS    IOS 15.4(3)M6        12/9/2018           
2      Cisco     WS-C3560E-48PD-SF    IOS 15.0(2)SE9       1/30/2014           
1      Cisco     WS-C3560E-48PD-SF    IOS 15.0(3)SE9       1/30/2014
```

Talking to some coworkers helped and I was finally able to come up with a game plan:
1. Assume that a unique device model could only belong to one vendor. We don't expect to have a model (such as `WS-C3560E-48PD-SF` that will show up under a row with vendor `Cisco` and then another row with vendor `Juniper`.
2. Convert the csv to a Pandas dataframe.  This will make it easier to sort/filter.
3. Sort by unique device Model types and make this its own data structure.
4. Sort by unique software versions within the data structure of unique models.
5. Put this information into a datastructure that is easy to print (add vendor and EoS info as well).
6. Bob's your uncle!

Maybe I should go over the data structures I used along the way...

Start with simplified csv for test/demo purposes (K.I.S.S.):
```
Device EoX Report Table : 2018-12-10 08:29:00 -0500 - 2018-12-11 08:29:00 -0500 (-5h),,,,,,,,,,,,,,,,,,,,
#,Device Name,IP Address,Vendor,Model,Operating System,EoX Device Entry,Device Status,EoX Software Entry,Software Status,OS Image,Memory,Flash,Created,System Contact,Model ID,Agent ID,Object ID,Device End-of-Sales,Device End-of-Service,Device End-of-Life
4,Switch004,172.16.2.40,Cisco,CISCO3925-CHASSIS,IOS 15.4(3)M6,CISCO3925-CHASSIS,EoX,IOS 15.4(3)M,EoX,flash0:c3900-universalk9-mz.SPA.154-3.M6.bin,"1,024",978,12/1/2018 0:00,Guido van Rossum,9.1.1042,"1,005","1,387",12/9/2017 0:00,12/9/2018 0:00,12/31/2022 0:00
30,Switch030,172.32.94.153,Cisco,WS-C3560E-48PD-SF,IOS 15.0(3)SE9,WS-C3560E-48PD-SF,EoX,IOS 15.0(2)SE,EoX,flash:c3560e-universalk9-mz.150-2.SE9.bin,128,61,10/30/2018 18:12,Guido van Rossum,9.1.796,"1,005","1,125",1/30/2013 0:00,1/30/2014 0:00,1/31/2018 0:00
31,Switch031,172.32.94.154,Cisco,WS-C3560E-48PD-SF,IOS 15.0(2)SE9,WS-C3560E-48PD-SF,EoX,IOS 15.0(2)SE,EoX,flash:c3560e-universalk9-mz.150-2.SE9.bin,128,61,10/30/2018 18:12,Guido van Rossum,9.1.796,"1,005","1,128",1/30/2013 0:00,1/30/2014 0:00,1/31/2018 0:00
32,Switch031,172.32.94.154,Cisco,WS-C3560E-48PD-SF,IOS 15.0(2)SE9,WS-C3560E-48PD-SF,EoX,IOS 15.0(2)SE,EoX,flash:c3560e-universalk9-mz.150-2.SE9.bin,128,61,10/30/2018 18:12,Guido van Rossum,9.1.796,"1,005","1,128",1/30/2013 0:00,1/30/2014 0:00,1/31/2018 0:00
```

First the Pandas dataframe:
```
  Device Name Vendor              Model Operating System Device End-of-Service
0   Switch004  Cisco  CISCO3925-CHASSIS    IOS 15.4(3)M6        12/9/2018 0:00
1   Switch030  Cisco  WS-C3560E-48PD-SF   IOS 15.0(3)SE9        1/30/2014 0:00
2   Switch031  Cisco  WS-C3560E-48PD-SF   IOS 15.0(2)SE9        1/30/2014 0:00
3   Switch031  Cisco  WS-C3560E-48PD-SF   IOS 15.0(2)SE9        1/30/2014 0:00
```

Next, create dictionary of unique device models:
```
{'CISCO3925-CHASSIS': <rest of dataframe info>,
 'WS-C3560E-48PD-SF': <rest of dataframe info>}
```

Next, create separate dictionaries for every unique software version within each unique device model:
```
{'IOS 15.4(3)M6': <rest of dataframe info>}
-----------
{'IOS 15.0(2)SE9': <rest of dataframe info>,
 'IOS 15.0(3)SE9': <rest of dataframe info>}
```

Convert these individual dictionaries to a master list of dictionaries to be printed and add pertinent information (count/EoS):
```
[{'Count': 1,
  'EoL': '12/9/2018',
  'Model': 'CISCO3925-CHASSIS',
  'OS': 'IOS 15.4(3)M6',
  'Rest': <rest of dataframe info>,
  'Vendor': 'Cisco'},
 {'Count': 2,
  'EoL': '1/30/2014',
  'Model': 'WS-C3560E-48PD-SF',
  'OS': 'IOS 15.0(2)SE9',
  'Rest': <rest of dataframe info>,
  'Vendor': 'Cisco'},
 {'Count': 1,
  'EoL': '1/30/2014',
  'Model': 'WS-C3560E-48PD-SF',
  'OS': 'IOS 15.0(3)SE9',
  'Rest': <rest of dataframe info>,
  'Vendor': 'Cisco'}]
```

Print this information so it is easier to read:
```
Count  Vendor    Model                Software             End of Service      
1      Cisco     CISCO3925-CHASSIS    IOS 15.4(3)M6        12/9/2018           
2      Cisco     WS-C3560E-48PD-SF    IOS 15.0(2)SE9       1/30/2014           
1      Cisco     WS-C3560E-48PD-SF    IOS 15.0(3)SE9       1/30/2014
```

## ___Variable Naming/Program Structure___

This program uses the same variable naming, comment and program structure as last month's submission for, more information, see the section with the same name (Variable Naming/Program Structure) in the following link:
https://github.com/johnnywilkes/NPL_NOV_2018_TIME/blob/master/README.md


## ___Possible Refactoring/Feature Releases___

 - I ran out of time and wanted to do either of the bonus challenge.  However, my philosophy when challenged with either having to well document a solution or add additional features, is always to make the documentation right.
 - For the base challenge, I used what little knowledge I had of Pandas and went back and forth between using Pandas dataframe and python data structures (lists, dictionaries or a combination of both).  I know that I know have completed with task without Pandas, or solely relied on Pandas alone, but didn't have time to figure out either.  If I had the time I would like to figure out both of these options and maybe give the user a choice of which they wanted to use.
 
