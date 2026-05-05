# Open HRMS / ohrms_core expects pandas (see __manifest__ external_dependencies).
FROM odoo:19.0
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pandas \
    && rm -rf /var/lib/apt/lists/*
USER odoo
