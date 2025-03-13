#!/bin/bash

# Get pcn from http request in the future
export pcn="123681"
export pcn_list="123681"
# export pcn_list="123681,300758"
export username=$(</etc/lastpass/username)
export password=$(</etc/lastpass/password)
export username2=$(</etc/lastpass/username2)
export password2=$(</etc/lastpass/password2)
export username3=$(</etc/lastpass/username3)
export password3=$(</etc/lastpass/password3)
export username4=$(</etc/lastpass/username4)
export password4=$(</etc/lastpass/password4)
export MYSQL_HOST=$(</etc/lastpass/MYSQL_HOST)
export MYSQL_PORT=$(</etc/lastpass/MYSQL_PORT)
export AZURE_DW=$(</etc/lastpass/AZURE_DW)
export MYSQL_HOST=$(</etc/lastpass/MYSQL_HOST)
export MYSQL_PORT=$(</etc/lastpass/MYSQL_PORT)
export AZURE_DW=$(</etc/lastpass/AZURE_DW)
export MONGO_HOST=$(</etc/lastpass/MONGO_HOST)
export MONGO_PORT=$(</etc/lastpass/MONGO_PORT)
export MONGO_DB=$(</etc/lastpass/MONGO_DB)

printf "\npcn: $pcn" 
printf "\npcn_list: $pcn_list" 
printf "\nusername: $username" 
printf "\npassword: $password" 
printf "\nusername2: $username2" 
printf "\npassword2: $password2" 
printf "\nusername3: $username3" 
printf "\npassword3: $password3"
printf "\nusername4: $username4" 
printf "\npassword4: $password4"
printf "\nMYSQL_HOST: $MYSQL_HOST" 
printf "\nMYSQL_PORT: $MYSQL_PORT" 
printf "\nAZURE_DW: $AZURE_DW" 
printf "\nMONGO_HOST: $MONGO_HOST" 
printf "\nMONGO_PORT: $MONGO_PORT" 
printf "\nMONGO_DB: $MONGO_DB" 

