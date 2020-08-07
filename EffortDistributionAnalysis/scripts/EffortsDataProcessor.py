import pandas as pd
import numpy as np


class EffortsDataProcessor:
    # Load raw data (including coordinators)
    def __init__(self, inputfile, start_date, end_date):
        self.start_dt = start_date
        self.end_dt = end_date
        self.LoadCSV(inputfile)
        #self.FilterDataInDateRange()
        self.UpdateWorkStream()
        self.UpdateCategory()
        self.UpdateActivityDsplayName()
        self.UpdateMemberRole()
        self.UpdateCategoriesForManagementReports()
        self.DistributeScrumKanbanEfforts()

    # Load raw data (including coordinators)
    def LoadCSV(self, inputfile):
        headers = ['Team','WorkStream','Iteration','Member','Date','Activity','Effort']
        dtypes = {'Team': 'str','WorkStream': 'str','Iteration': 'str','Member': 'str','Date': 'str','Activity': 'str','Effort': 'float'}
        parse_dates = ['Date']
        self.base_df = pd.read_csv(inputfile, sep=',', skiprows=1, names=headers, dtype=dtypes, parse_dates=parse_dates)

    # Filter out the data in given date range
    def FilterDataInDateRange(self):
        mask = (self.base_df['Date'] >= self.start_dt) & (self.base_df['Date'] <= self.end_dt)
        self.base_df = self.base_df.loc[mask]

    # Update the workstream - Do not update where team is coordinators
    def UpdateWorkStream(self):
        df = self.base_df
        mask = (df['Team'] != 'Coordinators')
        team_df = df.loc[mask]
        mask = (df['Team'] == 'Coordinators')
        coordinator_df = df.loc[mask]
        mapfile = '../maps/map-team-workstream.csv'
        headers = ['Team','MappedWorkStream']
        dtypes = {'Team': 'str','MappedWorkStream': 'str'}
        workstream_map_df = pd.read_csv(mapfile, sep=',', skiprows=1, names=headers, dtype=dtypes)
        team_df = pd.merge(team_df, workstream_map_df, how='left', on='Team')
        team_df['WorkStream'] = team_df['MappedWorkStream']
        team_df = team_df.drop( columns = ['MappedWorkStream'])
        self.base_df = pd.concat([team_df, coordinator_df], ignore_index=True)


    # Update the Category
    def UpdateCategory(self):
        mapfile = '../maps/map-activity-category.csv'
        headers = ['Activity','Category']
        dtypes = {'Activity': 'str','Category': 'str'}
        category_map_df = pd.read_csv(mapfile, sep=',', skiprows=1, names=headers, dtype=dtypes)
        self.base_df = pd.merge(self.base_df, category_map_df, how='left', on='Activity')

    # Update the Activity Display Name
    def UpdateActivityDsplayName(self):
        mapfile = '../maps/map-activity-displayname.csv'
        headers = ['Activity','DisplayName']
        dtypes = {'Activity': 'str','DisplayName': 'str'}
        displayname_map_df = pd.read_csv(mapfile, sep=',', skiprows=1, names=headers, dtype=dtypes)
        self.base_df = pd.merge(self.base_df, displayname_map_df,how='left',  on='Activity')

    # Update member role
    def UpdateMemberRole(self):
        mapfile = '../maps/map-member-role.csv'
        headers = ['Member','Role']
        dtypes = {'Member': 'str','Role': 'str'}
        member_role_map_df = pd.read_csv(mapfile, sep=',', skiprows=1, names=headers, dtype=dtypes)
        self.base_df = pd.merge(self.base_df, member_role_map_df, how='left',on='Member')

    # Update Categories For Management Reports
    def UpdateCategoriesForManagementReports(self):
        mapfile = '../maps/map-category-useinreport.csv'
        headers = ['Category','UseInReports']
        dtypes = {'Category': 'str','UseInReports': 'str'}
        category_useinreport_map_df = pd.read_csv(mapfile, sep=',', skiprows=1, names=headers, dtype=dtypes)
        self.base_df = pd.merge(self.base_df, category_useinreport_map_df,  how='left', on='Category')


    # Distribute Scrum and kanban efforts in Maintenanc and Innovation 
    def DistributeScrumKanbanEfforts(self):
        non_scrum_kanban_df = self.base_df
        mask = (non_scrum_kanban_df['Activity'] != 'Scrum/Kanban Meetings')
        non_scrum_kanban_df = non_scrum_kanban_df.loc[mask]

        mask = (non_scrum_kanban_df['Category'] == 'Product Innovation') | (non_scrum_kanban_df['Category'] == 'Product Maintenance & Support')
        df_pi_pm = non_scrum_kanban_df.loc[mask]
        df1 = df_pi_pm.groupby(['WorkStream', 'Category'], as_index=False)[['Effort']].sum()
        df2 = df_pi_pm.groupby(['WorkStream'], as_index=False)[['Effort']].sum()
        df3 = pd.merge(df1, df2 , how='left',on='WorkStream')
        df3['Efforts_pct'] = df3['Effort_x'] / df3['Effort_y']

        mask = (df3['Category'] == 'Product Innovation') 
        innovation_pct_df = df3.loc[mask]
        innovation_pct_df = innovation_pct_df.drop( columns = ['Category','Effort_x','Effort_y'])

        mask = (df3['Category'] == 'Product Maintenance & Support') 
        maintenance_pct_df = df3.loc[mask]
        maintenance_pct_df = maintenance_pct_df.drop( columns = ['Category','Effort_x','Effort_y'])

        scrum_kanban_df = self.base_df
        mask = (scrum_kanban_df['Activity'] == 'Scrum/Kanban Meetings')
        scrum_kanban_df = scrum_kanban_df.loc[mask]

        innovation_df = pd.merge(scrum_kanban_df, innovation_pct_df ,how='left',  on='WorkStream')
        maintenance_df = pd.merge(scrum_kanban_df, maintenance_pct_df ,how='left',  on='WorkStream')

        innovation_df['Effort'] = innovation_df['Effort'] * innovation_df['Efforts_pct']
        maintenance_df['Effort'] = maintenance_df['Effort'] * maintenance_df['Efforts_pct']
        innovation_df = innovation_df.drop( columns = ['Efforts_pct'])
        maintenance_df = maintenance_df.drop( columns = ['Efforts_pct'])

        innovation_df['Activity'] = 'IN_Scrum/Kanban Meetings'
        maintenance_df['Activity'] = 'MN_Scrum/Kanban Meetings'

        innovation_df['Category'] = 'Product Innovation'
        maintenance_df['Category'] = 'Product Maintenance & Support'
    
        self.base_df = pd.concat([non_scrum_kanban_df, innovation_df,maintenance_df], ignore_index=True, sort=False)


    def GetData(self):
        return (self.base_df)


