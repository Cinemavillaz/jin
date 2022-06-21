if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning master Repository"
  git clone https://github.com/Cinemavillaz/superman-2.git /superman-2
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO"
  git clone $UPSTREAM_REPO /superman-2
fi
cd /superman-2
pip3 install -U -r requirements.txt
echo "Starley ♡ Harley"
python3 bot.py
