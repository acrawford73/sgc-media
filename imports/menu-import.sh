#!/bin/bash
# A menu driven shell script template 
## ----------------------------------
# Step #1: Define variables
# ----------------------------------
EDITOR=vim
PASSWD=/etc/passwd
RED='\033[0;41;30m'
STD='\033[0;0;39m'

# ----------------------------------
# Step #2: User defined function
# ----------------------------------
pause(){
  read -p "Press [Enter] key to continue..." fackEnterKey
}

one(){
	echo "Importing all JSON data to Database..."
	python3 imports.py all
	pause
}

two(){
	echo "Importing Countries..."
	python3 imports.py country
	pause
}

three(){
	echo "Importing Video Formats..."
	python3 imports.py vf
	pause
}

four(){
	echo "Importing Video Services..."
	python3 imports.py vs
	pause
}

five(){
	echo "Importing Video Genres..."
	python3 imports.py vg
	pause
}
 
six(){
	echo "Importing Audio Formats..."
	python3 imports.py vf
	pause
}

seven(){
	echo "Importing Audio Services..."
	python3 imports.py vs
	pause
}

eight(){
	echo "Importing Audio Genres..."
	python3 imports.py vg
	pause
}

nine(){
	echo "Importing Photo Formats..."
	python3 imports.py pf
	pause
}

ten(){
	echo "Importing Photo Services..."
	python3 imports.py ps
	pause
}

eleven(){
	echo "Importing Document Formats..."
	python3 imports.py df
	pause
}

twelve(){
	echo "Importing Languages..."
	python3 imports.py lang
	pause
}

thirteen(){
	echo "Importing Countries..."
	python3 imports.py cs
	pause
}

fourteen(){
	echo "Importing Content Genres..."
	python3 imports.py cg
	pause
}

fifteen(){
	echo "Importing External ID Types..."
	python3 imports.py eit
	pause
}

sixteen(){
	echo "Importing Rating Sources..."
	python3 imports.py rs
	pause
}

seventeen(){
	echo "Importing Parental Ratings..."
	python3 imports.py pr
	pause
}

eightteen(){
	echo "Importing Ratings..."
	python3 imports.py rating
	pause
}

nineteen(){
	echo "Importing Search Genres..."
	python3 imports.py sg
	pause
}


# function to display menus
show_menus() {
	clear
	echo "----------------------------------"	
	echo " SGC-MEDIA STATIC DATA IMPORTER"
	echo " WARNING: Run any menu once only"
	echo "----------------------------------"
	echo
	echo "1. All Data for Fresh Install"
	echo
	echo "Schema: MEDIA"
	echo
	echo "2. Countries"
	echo "3. Video Formats"
	echo "4. Video Services"
	echo "5. Video Genres"
	echo "6. Audio Formats"
	echo "7. Audio Services"
	echo "8. Audio Genres"
	echo "9. Photo Formats"
	echo "10. Photo Services"
	echo "11. Document Formats"
	echo
	echo "Schema: ROKU_CONTENT"
	echo
	echo "12. Language"
	echo "13. Countries"
	echo "14. Content Genres"
	echo "15. External IDs"
	echo "> Do these rating tables in order: 16, 17, 18"
	echo "16. Rating Sources"
	echo "17. Parental Ratings"
	echo "18. Ratings"
	echo
	echo "Schema: ROKU_SEARCH"
	echo
	echo "19. Search Genres"
	echo
	echo "99. Exit"
	echo
}
# read input from the keyboard and take a action
# invoke the one() when the user select 1 from the menu option.
# invoke the two() when the user select 2 from the menu option.
# Exit when user the user select 3 form the menu option.
read_options(){
	local choice
	read -p "Enter choice [ 1 - 99] " choice
	case $choice in
		1) one ;;
		2) two ;;
		3) three ;;
		4) four ;;
		5) five ;;
		6) six ;;
		7) seven ;;
		8) eight ;;
		9) nine ;;
		10) ten ;;
		11) eleven ;;
		12) twelve ;;
		13) thirteen ;;
		14) fourteen ;;
		15) fifteen ;;
		16) sixteen ;;
		17) seventeen ;;
		18) eighteen ;;
		19) nineteen ;;
		20) twenty ;;
		99) exit 0;;
		*) echo -e "${RED}Error...${STD}" && sleep 2
	esac
}
 
# ----------------------------------------------
# Step #3: Trap CTRL+C, CTRL+Z and quit singles
# ----------------------------------------------
trap '' SIGINT SIGQUIT SIGTSTP
 
# -----------------------------------
# Step #4: Main logic - infinite loop
# ------------------------------------
while true
do
	show_menus
	read_options
done
