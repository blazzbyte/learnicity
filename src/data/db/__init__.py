import streamlit as st
from .db import Database
from src.core.config import logger

db = Database()

__all__ = ["db"]