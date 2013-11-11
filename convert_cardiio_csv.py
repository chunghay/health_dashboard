import csv
import datetime


def main():
  # Initialize variables.
  fileName = 'Data_files/CardiioData.csv'

  # Headers for data of interest.
  date  = 'Date'
  time  = 'Time'
  hr    = 'HR (bpm)'
  state = 'State'
  notes = 'Notes'

  dateIdx  = ''
  timeIdx  = ''
  hrIdx    = ''
  stateIdx = ''
  notesIdx = ''

  with open(fileName, "rU") as f:
    rows = csv.reader(f)
    rownum = 0

    for row in rows:
      # Get indices of desired parameters from the header row.
      if rownum == 1:
        colnum = 0
        for col in row:
          # Remove any whitespace at front and end of entry.
          col = col.rstrip().lstrip()
          
          if col == date:
            dateIdx = colnum
          if col == time:
            timeIdx = colnum
          if col == hr:
            hrIdx = colnum
          if col == state:
            stateIdx = colnum
          if col == notes:
            notesIdx = colnum
          colnum += 1

        if dateIdx == '' or timeIdx == '' or hrIdx == '' or stateIdx == '' or notesIdx == '':
          print "One or more of the following headers are missing..."
          print "dateIdx: %s, timeIdx: %s, hrIdx: %s, stateIdx: %s, notesIdx: %s" % (dateIdx, timeIdx, hrIdx, stateIdx, notesIdx)

      # For data rows, get desired values.
      elif rownum > 1:
       
          # Get Unix timestamp.
          mdy = row[dateIdx].split('/')
          hms = row[timeIdx].split(':')
          d = datetime.datetime(int(mdy[2]), int(mdy[0]), int(mdy[1]), int(hms[0]), int(hms[1]), int(hms[2]))
          unixTime = d.strftime('%s')

          # Output data.
          if row[stateIdx].rstrip().lstrip() == 'rest':
            key = 'qs.cardio.heartrate_bmp.rest'
          elif row[stateIdx].rstrip().lstrip() == 'active':
            key = 'qs.cardio.heartrate_bmp.active'
          else:
            key = 'qs.cardio.heartrate_bmp.misc'
          print "%s %s %s" %(key, row[hrIdx], unixTime)

          """if len(row[notesIdx]) > 0: 
            key = 'qs.cardio.heartrate_bmp.notes'
            print "%s %s %s" %(key, row[notesIdx], unixTime)"""

      rownum += 1


if __name__ == '__main__':
  main()