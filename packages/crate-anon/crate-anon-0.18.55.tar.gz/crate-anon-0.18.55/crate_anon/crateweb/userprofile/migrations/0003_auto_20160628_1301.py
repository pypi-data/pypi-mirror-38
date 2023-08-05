#!/usr/bin/env python

"""
crate_anon/crateweb/userprofile/migrations/0003_auto_20160628_1301.py

===============================================================================

    Copyright (C) 2015-2018 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

**Userprofile app, migration 0003.**

"""

# Generated by Django 1.9.7 on 2016-06-28 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_sql_scratchpad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='collapse_at',
            new_name='collapse_at_len',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='collapse_at_n_lines',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='Number of lines beyond which result/query field starts collapsed (0 for none)'),  # noqa
        ),
    ]
