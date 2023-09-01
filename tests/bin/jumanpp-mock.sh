#!/usr/bin/env bash

while true; do
  read -r line

  if [ "$line" = "time consuming input" ]; then
    sleep 5
  fi

  if [ "$line" = "error causing input" ]; then
    echo 'エラー1' >&2
    echo 'エラー2' >&2
    exit 0
  fi

  if [ "$line" = "knp time consuming input" ]; then
    echo '# knp time consuming input'
    echo 'EOS'
    continue
  fi

  if [ "$line" = "knp error causing input" ]; then
    echo '# knp error causing input'
    echo 'EOS'
    continue
  fi

  echo 'こんにちは こんにちは こんにちは 感動詞 12 * 0 * 0 * 0 "代表表記:こんにちは/こんにちは"'
  echo 'さようなら さようなら さようなら 感動詞 12 * 0 * 0 * 0 "代表表記:さようなら/さようなら"'
  echo 'EOS'
done
