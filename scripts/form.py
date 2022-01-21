from flask import Flask, Blueprint, render_template, request, flash
app_form = Blueprint("simple", __name__, template_folder="templates")