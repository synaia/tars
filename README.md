### TARS, inspired by the interstellar robot from the movie "Interstellar"


#### Setup main project (fast-api)
```shell 
git clone ....
conda create --name tars_env python=3.10 -y
conda activate tars_env
cd tars
pip install -r requeriments.txt
```

#### Pre-requ for run integration (odoo) fast-api
create a .secret file on tars directory with the following structure:
```shell
PASSWORD='<password here>'
```

#### Setup prescreening front-end project (react-node)

```shell 
cd tars/recruitment/prescreening
npm install
# For Windows OS
npm config set script-shell "C:\\Program Files\\git\\bin\\bash.exe" 
npm run start
```

Setting Ubuntu time.
timedatectl list-timezones | grep -i paz
sudo timedatectl set-timezone America/La_Paz

sudo vim /etc/postgresql/14/main/postgresql.conf -> change timezone
sudo systemctl restart postgresql





INSTALL conda Digital Ocean

curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
file Miniconda3-latest-Linux-x86_64.sh 
chmod 755 Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh
sudo ln -s /home/wilton/miniconda3/bin/conda /usr/bin/conda

/usr/lib/postgresql/14/bin/postgres --version
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt install postgresql-14-pgvector

CREATE EXTENSION vector;
BEGIN;

CREATE TABLE IF NOT EXISTS public.company_info
(
    id bigserial NOT NULL,
    text text COLLATE pg_catalog."default",
    embedding vector,
    CONSTRAINT company_info_pkey PRIMARY KEY (id)
);
END;



![image](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhzgwetd93YNGiy-FZ0HAs807Q6_walEUZqnt7TNtN-3RdAEOv075dnd0KNw7Nlo98KI-5S7XVtpmCPTAshV0OlBmbIZu-rESuwvWpE4eVMb7qDKCce7oZ-lMA1td8CnlsLuZR88vgly-k/s320/cooper+and+tars.jpg)