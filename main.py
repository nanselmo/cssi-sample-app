#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

def pig_latinize_word(word):
  vowels = ["a", "e", "i", "o", "u"]
  if word[0].lower() in vowels:
    pig_latin_word = word + "ay"
  else:
    if word[1].lower() not in vowels:
      first_letters = word[:2]
      rest_of_word = word[2:]
      pig_latin_word = rest_of_word + first_letters + "ay"
    else:
      first_letter = word[0]
      rest_of_word = word[1:]
      pig_latin_word = rest_of_word + first_letter + "ay"
  return pig_latin_word


def pig_latinize_phrase(phrase):
  words = phrase.split(" ")
  pl_words = []
  for word in words:
    pl_words.append(pig_latinize_word(word))
  final_string = " ".join(pl_words)
  return final_string

current_directory=jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        hello_template=current_directory.get_template("templates/hello.html")
        self.response.write(hello_template.render())
    def post(self):
        results_template=current_directory.get_template("templates/results.html")
        name = self.request.get('user_name')
        template_vars={'the_name':name}
        self.response.write(results_template.render(template_vars))

class CountHandler(webapp2.RequestHandler):
    def get(self):
        for number in range(1,11):
            self.response.write(str(number) + " ")

class PigHandler(webapp2.RequestHandler):
    def get(self):
        pig_template=current_directory.get_template("templates/pig.html")
        self.response.write(pig_template.render(my_vars))
    def post(self):
        pig_template=current_directory.get_template("templates/pig.html")
        new_word=pig_latinize_phrase(self.request.get("input_word"))
        my_vars={'final_word':new_word}
        self.response.write(pig_template.render(my_vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/count', CountHandler),
    ('/piglatin',PigHandler)
], debug=True)
