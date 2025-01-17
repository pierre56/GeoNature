from itertools import chain, product

from jinja2 import Template
from flask import current_app

from pypnusershub.db.models import User

from geonature.core.notifications.models import (
    Notification,
    NotificationCategory,
    NotificationRule,
    NotificationTemplate,
)
from geonature.utils.env import db
from geonature.core.notifications.tasks import send_notification_mail


def dispatch_notifications(
    code_categories, id_roles, title=None, url=None, *, content=None, context={}
):
    if not current_app.config["NOTIFICATIONS_ENABLED"]:
        return

    categories = chain.from_iterable(
        [
            NotificationCategory.query.filter(NotificationCategory.code.like(code)).all()
            for code in code_categories
        ]
    )
    roles = [User.query.get(id_role) for id_role in id_roles]

    for category, role in product(categories, roles):
        dispatch_notification(category, role, title, url, content=content, context=context)


def dispatch_notification(category, role, title=None, url=None, *, content=None, context={}):
    if not title:
        title = category.label

    # add role, title and url to rendering context
    context = {"role": role, "title": title, "url": url, **context}

    rules = NotificationRule.query.filter(
        NotificationRule.id_role == role.id_role,
        NotificationRule.code_category == category.code,
    )
    for rule in rules.all():
        if content:
            notification_content = content
        else:
            # get template for this method and category
            notification_template = NotificationTemplate.query.filter_by(
                category=category,
                method=rule.method,
            ).one_or_none()
            if not notification_template:
                continue
            notification_content = Template(notification_template.content).render(context)
            # if no content break | content is
            if not notification_content.strip():
                continue

        if rule.code_method == "DB":
            send_db_notification(role, title, notification_content, url)
        elif rule.code_method == "EMAIL":
            send_mail_notification(role, title, notification_content)


def send_db_notification(role, title, content, url):
    # Save notification in database as UNREAD
    current_app.logger.info(f"Send database notification to {role}")
    notification = Notification(
        user=role,
        title=title,
        content=content,
        url=url,
        code_status="UNREAD",
    )
    db.session.add(notification)
    return notification


def send_mail_notification(role, title, content):
    if not role.email:
        return
    current_app.logger.info(f"Send email notification to {role} ({role.email})")
    send_notification_mail.delay(f"[GeoNature] {title}", content, role.email)
